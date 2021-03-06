type 'a stream = Cons of 'a * (unit -> 'a stream)

let rec ands (blist: bool list) = 
  match blist with
  | [ ] -> true
  | b :: bs -> if b then ands bs else false

let rec ones = Cons (1, fun () -> ones)

let rec squares_from (n:int) :int stream= Cons (n*n, fun () -> squares_from (n+1))

let rec drop (n:int) (s : 'a stream) : ('a stream) =
  if n = 0 then s
  else match s with
       | Cons (_, tl) -> drop (n-1)  (tl ()) 

let rec drop_until (f: 'a -> bool) (s:'a stream): 'a stream = 
  match s with 
  | Cons (v, tl) -> if f v then s                   (*first occurance is true, so return whole stream*) 
		    else drop_until f (tl ())

let rec map (f: 'a -> 'b) (s: 'a stream) : 'b stream = 
  match s with 
  | Cons (v, tl) -> Cons (f v, fun () -> map f (tl ()))



let rec from n = Cons ( n, fun () -> from (n+1) )
let nats = from 1
(*check if we can use nats and from1 on squares again!, and also ask about tl () and () tl*)
let squares_again = map (fun x -> x * x) nats

let sqrt_approximations (n:float): float stream = 
  let rec sqhlpr low up = 
    let guess = (low +. up) /. 2.0  in 
    if (guess *. guess) > n then Cons (guess, fun () -> (sqhlpr low guess))
    else Cons (guess, fun () -> (sqhlpr guess up))
  in sqhlpr 1.0 n


(*might be able to use take drop instead*)
let rec epsilon_diff (ep:float) (s: float stream): float = 
  match s with
  | Cons (v, tl) -> match (tl ()) with 
		    | Cons (v2, _) -> if ep > Float.abs (v -. v2) then v2 else epsilon_diff ep (tl ()) 

let rough_guess = epsilon_diff 1.0 (sqrt_approximations 50.0) 
let precise_calculation = epsilon_diff 0.00001 (sqrt_approximations 50.0) 

let head (s: 'a stream) : 'a = match s with
  | Cons (v, _) -> v

let tail (s: 'a stream) : 'a stream = match s with
  | Cons (_, tl) -> tl ()


(*  Explanation for why sqrt_threshold is more accurate than using epsilon_diff
    epsilon_diff takes successive approximation values from the stream of approximations, 
    it then computes the difference between them to see if it is within 'epsilon' accuracy.
    Whereas sqrt_threshold only takes one approximation, reducing the number of 'approximated
    values' and then squares that square root, and takes the difference compared to the original 
    number to see if it is within the threshold (margin of difference), making it more accurate as
    it tests for correctness. 
*)

let sqrt_threshold (v:float) (t:float): float = 
  let rec helper (sqrt:float stream) =
  match (map (fun s -> Float.abs ((s *. s) -.v) < t) sqrt) with
  | Cons (true, _) -> (head sqrt)  
  | Cons (false, _) -> helper (tail sqrt)
  in helper (sqrt_approximations v)




(* ######## Extra Helper functions ####### *)
let rec diminishing n= Cons (n, fun () -> diminishing (n/.2.0))

let rec take (n:int) (s : 'a stream) : ('a list) =
 if n = 0 then []
 else match s with
      | Cons (v, tl) -> v :: take (n-1) (tl ()) 

let squares = squares_from 1

let rec filter (f: 'a -> bool) (s: 'a stream) : 'a stream =
  match s with
  | Cons (hd, tl) ->
     let rest = (fun () -> filter f (tl ()))
     in
     if f hd then Cons (hd, rest) else rest ()

(*#### End of Extra helper functions #####*)
