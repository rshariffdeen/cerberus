(declare-fun output!i32!obs!0 () (Array (_ BitVec 32) (_ BitVec 8) ) )
(assert (and (bvslt (concat  (select  output!i32!obs!0 (_ bv3 32) ) (concat  (select  output!i32!obs!0 (_ bv2 32) ) (concat  (select  output!i32!obs!0 (_ bv1 32) ) (select  output!i32!obs!0 (_ bv0 32) ) ) ) ) (_ bv30 32))  (bvsgt (concat  (select  output!i32!obs!0 (_ bv3 32) ) (concat  (select  output!i32!obs!0 (_ bv2 32) ) (concat  (select  output!i32!obs!0 (_ bv1 32) ) (select  output!i32!obs!0 (_ bv0 32) ) ) ) ) (_ bv0 32)) ))
