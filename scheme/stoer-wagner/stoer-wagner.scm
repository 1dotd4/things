;; Hewwoo
;; https://www.cs.tau.ac.il/~zwick/grad-algo-08/gmc.pdf

(define (global-min-cut graph)
  (let ((nodes (graph-nodes graph)))
    (if (<= (length nodes) 2)
        nodes
        (let* ((st-cut (st-min-cut graph))
               (second-cut (global-min-cut (graph-contraction graph (cdr st-cut)))))
          (if (<= (graph-weight (st-get-graph st-cut))
                  (graph-weight second-cut))
              (car st-cut)
              second-cut
            )))))

;; => (cut, first-node, second-node)
(define (st-min-cut graph)
  (define (sort-by-max-weight ...)
    )
  (until (graph-eq )

  )))

;; Dataset 1:
;; [[1], [2]]
;; 30, 56

;; Dataset 9:
;; [[1], [26]]

;; hint:
;; st_mincut: 3056 8 5
;; st_mincut: 7974 8 6
;; st_mincut: 14772 7 4
;; st_mincut: 10186 8 10
;; st_mincut: 12372 7 3
;; st_mincut: 15973 7 8
;; st_mincut: 18615 9 7
;; st_mincut: 13895 2 9
;; Base case: 9091 1 2
;; mincut weight: 3056
