"""CPU oracle checks. Independent scalar reference uses stdlib math only.
Never import or execute StressDream, torch, learned heads, renderer or weights.
"""
import itertools
import math
from pathlib import Path
import tempfile
import unittest

import numpy as np
import ORACLE_IMPLEMENTATION as oracle


def scalar_reference(initial, actions, signs, speed=1.0, dt=0.05, radius=0.25):
    x,y,theta=map(float,initial)
    values=[x*x+y*y-radius*radius]
    points=[(x,y,theta)]
    for a,d in zip(actions,signs):
        dx=speed*dt*math.cos(theta)
        dy=speed*dt*math.sin(theta)
        next_theta=theta+dt*float(d)*float(a)
        x,y,theta=x+dx,y+dy,next_theta
        values.append(x*x+y*y-radius*radius)
        points.append((x,y,theta))
    return min(values),points


class OracleTests(unittest.TestCase):
    def test_update_order_uses_old_heading(self):
        path=oracle.replay([0,0,0],[1.25],[1])
        np.testing.assert_array_equal(path[1,:2],[0.05,0])
        self.assertEqual(path[1,2],0.0625)
        self.assertNotAlmostEqual(path[1,1],0.05*math.sin(0.0625),places=12)

    def test_turn_sign_and_second_position(self):
        a=oracle.replay([0,0,0],[1.25,0],[1,1])
        b=oracle.replay([0,0,0],[1.25,0],[-1,1])
        self.assertGreater(a[2,1],0)
        self.assertLess(b[2,1],0)
        np.testing.assert_allclose(a[:,0],b[:,0],rtol=0,atol=1e-15)

    def test_score_sign_and_boundary(self):
        s=np.array([[0,0,0],[0.25,0,0],[0.5,0,0]],dtype=np.float64)
        np.testing.assert_array_equal(oracle.safety(s),[-0.0625,0,0.1875])
        r=oracle.enumerate_query([0.25,0,0],[0])
        self.assertTrue(r['support_failure'])
        self.assertTrue(r['boundary_ambiguous'])
        self.assertEqual(r['q_star'],0)
        np.testing.assert_array_equal(-oracle.safety(s),[0.0625,0,-0.1875])

    def test_initial_state_is_included(self):
        r=oracle.enumerate_query([0,0,0],[0,0,0])
        self.assertEqual(r['q_star'],-0.0625)
        self.assertEqual(r['witness_min_time'],0)

    def test_support_cardinality_and_branch_ids(self):
        d=oracle.disturbance_sequences(12)
        self.assertEqual(d.shape,(4096,12))
        self.assertEqual(np.unique(d,axis=0).shape[0],4096)
        np.testing.assert_array_equal(d[0],np.ones(12,dtype=np.int8))
        np.testing.assert_array_equal(d[1],[-1]+[1]*11)
        np.testing.assert_array_equal(d[-1],-np.ones(12,dtype=np.int8))

    def test_independent_product_probability_and_mass(self):
        ds=oracle.disturbance_sequences(12)
        for p in (0.2,0.4):
            w=oracle.branch_probabilities(ds,p)
            self.assertTrue(np.all(w>0))
            self.assertAlmostEqual(w.sum(),1,places=13)
            self.assertAlmostEqual(w[ds[:,0]==-1].sum(),p,places=13)
            self.assertAlmostEqual(w[(ds[:,0]==-1)&(ds[:,1]==-1)].sum(),p*p,places=13)

    def test_zero_action_closed_form(self):
        state=[-0.75,0,0]
        r=oracle.enumerate_query(state,np.zeros(12))
        # End x=-.15, and approaching the obstacle throughout.
        self.assertAlmostEqual(r['q_star'],0.15**2-0.25**2,places=14)
        self.assertEqual(np.ptp(r['branch_min_safety']),0)
        self.assertEqual(r['witness_path'].dtype,np.float64)
        self.assertEqual(r['branch_min_safety'].dtype,np.float64)

    def test_vectorization_matches_independent_scalar_all_4096(self):
        ds=oracle.disturbance_sequences(12)
        for state,actions in [([-0.45,0,0.6],oracle.candidate_actions(12)[2]),
                              ([-0.75,0,1.0],oracle.candidate_actions(12)[3])]:
            result=oracle.enumerate_query(state,actions)
            scalar=np.array([scalar_reference(state,actions,d)[0] for d in ds],dtype=np.float64)
            np.testing.assert_allclose(result['branch_min_safety'],scalar,rtol=0,atol=2e-15)
            self.assertAlmostEqual(result['q_star'],float(scalar.min()),places=14)

    def test_independent_cartesian_enumerator_small_horizon(self):
        state=[-0.35,0,0.4];actions=[1.25,0,0.625,1.25]
        expected=sorted(scalar_reference(state,actions,d)[0] for d in itertools.product([-1,1],repeat=4))
        actual=sorted(oracle.enumerate_query(state,actions)['branch_min_safety'])
        np.testing.assert_allclose(expected,actual,rtol=0,atol=2e-15)

    def test_control_sign_symmetry_of_support(self):
        a=oracle.candidate_actions(12)[3]
        positive=oracle.enumerate_query([-0.6,0,0.4],a)
        negative=oracle.enumerate_query([-0.6,0,0.4],-a)
        np.testing.assert_array_equal(positive['branch_min_safety'],negative['branch_min_safety'][::-1])

    def test_heading_wrap_invariance(self):
        a=oracle.candidate_actions(12)[2]
        left=oracle.enumerate_query([-0.6,0,0.6],a)
        right=oracle.enumerate_query([-0.6,0,0.6+2*math.pi],a)
        np.testing.assert_allclose(left['branch_min_safety'],right['branch_min_safety'],rtol=0,atol=2e-15)

    def test_last_disturbance_cannot_change_position_score(self):
        r=oracle.enumerate_query([-0.6,0,0.4],oracle.candidate_actions(12)[2])
        np.testing.assert_array_equal(r['branch_min_safety'][:2048],r['branch_min_safety'][2048:])

    def test_witness_and_regret_for_all_frozen_queries(self):
        for c in oracle.frozen_config()['contexts']:
            results=[oracle.enumerate_query(c['state'],a) for a in oracle.candidate_actions(12)]
            best=max(r['q_star'] for r in results)
            for a,r in zip(oracle.candidate_actions(12),results):
                q,path=scalar_reference(c['state'],a,r['witness_delta'])
                np.testing.assert_allclose(path,r['witness_path'],rtol=0,atol=2e-15)
                self.assertAlmostEqual(q,r['q_star'],places=14)
                self.assertGreaterEqual(best-r['q_star'],-1e-15)

    def test_frozen_split_and_candidates(self):
        c=oracle.frozen_config()
        self.assertEqual(len(c['contexts']),24)
        self.assertEqual(sum(r['split']=='test' for r in c['contexts']),16)
        self.assertEqual(sum(r['split']=='calibration' for r in c['contexts']),8)
        self.assertEqual(sum(c['actions']['12']['A3']),7.5)
        self.assertEqual(c['actions']['12']['A3'][6],0)
        self.assertEqual(c['actions']['12']['A4'][6],1.25)
        self.assertEqual(c['actions']['16']['A3'][8],0)

    def test_invalid_inputs_are_rejected(self):
        for state,actions in [([0,0],[0]),([0,0,0],[1.26]),([math.nan,0,0],[0])]:
            with self.assertRaises(ValueError):oracle.enumerate_query(state,actions)
        for h in (0,17,1.2):
            with self.assertRaises(ValueError):oracle.disturbance_sequences(h)
        for p in (0,1):
            with self.assertRaises(ValueError):oracle.branch_probabilities(oracle.disturbance_sequences(2),p)

    def test_summary_is_json_serializable(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'raw') as temp:
            out=Path(temp)
            (out/'raw').mkdir()
            *_,summary=oracle.run_horizon(oracle.frozen_config(),12,out)
            self.assertIn('informative_test_counts',oracle.canonical_json(summary))


if __name__=='__main__':
    unittest.main(verbosity=2)
