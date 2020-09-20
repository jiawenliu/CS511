(declare-const p1 Bool)
(declare-const p2 Bool)
(declare-const p3 Bool)
(declare-const p4 Bool)

;;; parity CNF
(declare-fun phi (Bool Bool Bool Bool) Bool) 
(assert (= (phi p1 p2 p3 p4)
           (and (or (not p1) p2 p3 p4) (or p1 (not p2) p3 p4) (or p1 p2 (not p3) p4) (or p1 p2 p3 (not p4)) (or (not p1) (not p2) (not p3) p4) (or (not p1) p2 (not p3) (not p4)) (or (not p1) (not p2) p3 (not p4)) (or p1 (not p2) (not p3) (not p4)))))

;;; parity DNF
(declare-fun psi (Bool Bool Bool Bool) Bool)
(assert (= (psi p1 p2 p3 p4)
        (or 	(and (not p1) (not p2) (not p3) (not p4))
		(and p1 p2 p3 p4)
		(and p1 p2 (not p3) (not p4))
		(and p1 (not p2) p3 (not p4))
		(and (not p1) p2 p3 (not p4))
		(and p1 (not p2) (not p3) p4)
		(and (not p1) p2 (not p3) p4)
		(and (not p1) (not p2) p3 p4)
	)))


(declare-const x Bool)
(declare-const y Bool)
(declare-fun biconditional (Bool Bool) Bool)
(assert (= (biconditional x y)
	(and (=> x y) (=> y x)
	)))

;;; parity_biconditional

(declare-fun theta (Bool Bool Bool Bool) Bool)
(assert (= (theta p1 p2 p3 p4)
        (biconditional (biconditional (biconditional p1 p2) p3) p4
	)))




(assert (not (= (psi p1 p2 p3 p4) (phi p1 p2 p3 p4))))
(check-sat)

(assert (not (= (psi p1 p2 p3 p4) (theta p1 p2 p3 p4))))
(check-sat)
