use std::cmp::max;

pub fn karatsuba(x: i64, y: i64) -> i64 { 
    if x < 10 || y < 10 {
        return x * y;
    }

    let n = max(x.to_string().len(), y.to_string().len());
    let m = n / 2;

    let x_str = x.to_string();
    let x_split_at = x_str.len().saturating_sub(m);
    let (x_left_str, x_right_str) = x_str.split_at(x_split_at);
    let x_left: i64 = x_left_str.parse().unwrap_or(0);
    let x_right: i64 = x_right_str.parse().unwrap_or(0);

    let y_str = y.to_string();
    let y_split_at = y_str.len().saturating_sub(m);
    let (y_left_str, y_right_str) = y_str.split_at(y_split_at);
    let y_left: i64 = y_left_str.parse().unwrap_or(0);
    let y_right: i64 = y_right_str.parse().unwrap_or(0);

    let z2 = karatsuba(x_left, y_left);
    let z0 = karatsuba(x_right, y_right);
    let z1 = karatsuba(x_left+x_right, y_left+y_right) - z2 - z0;

    z2 * 10_i64.pow((2*m) as u32) + z1 * 10_i64.pow(m as u32) + z0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_karatsuba() {
        assert_eq!(karatsuba(323, 32312), 10436776);
        assert_eq!(karatsuba(1234, 5678), 7006652);
        assert_eq!(karatsuba(12, 34), 408);
        assert_eq!(karatsuba(99, 99), 9801);
    }
}