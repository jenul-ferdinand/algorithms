pub fn fib_iterative(n: i32) -> i32 {
    if n == 0 {
        0
    } else if n == 1 {
        1
    } else {
        let mut a = 0;
        let mut b = 1;

        for _ in 2..=n {
            let temp = a + b;
            a = b;
            b = temp;
        }

        b
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fib_base_cases() {
        assert_eq!(fib_iterative(0), 0);
        assert_eq!(fib_iterative(1), 1);
    }

    #[test]
    fn test_fib_small_values() {
        assert_eq!(fib_iterative(2), 1);
        assert_eq!(fib_iterative(3), 2);
        assert_eq!(fib_iterative(4), 3);
        assert_eq!(fib_iterative(5), 5);
        assert_eq!(fib_iterative(6), 8);
    }

    #[test]
    fn test_fib_larger_values() {
        assert_eq!(fib_iterative(10), 55);
        assert_eq!(fib_iterative(15), 610);
        assert_eq!(fib_iterative(20), 6765);
    }
}