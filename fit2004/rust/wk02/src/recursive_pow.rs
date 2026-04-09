
pub fn recursive_pow(value: i32, power: i32) -> i32 {
    if power == 0 { 
        return 1 
    } else if power == 1 {
        return value
    } else {
        if power % 2 == 0 {
            recursive_pow(value, power/2) * recursive_pow(value, power / 2)
        } else  {
            recursive_pow(value, power / 2) * recursive_pow(value, power / 2) * value
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_recursive_pow() {
        assert_eq!(recursive_pow(1, 1), 1);
        assert_eq!(recursive_pow(100, 0), 1);
        assert_eq!(recursive_pow(34, 3), 39304);
        assert_eq!(recursive_pow(2, 10), 1024);
        assert_eq!(recursive_pow(5, 4), 625);
    }
}