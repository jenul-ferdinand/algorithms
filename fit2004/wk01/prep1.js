function karatsuba(x, y) {
    let xStr = x.toString();
    let yStr = y.toString();

    // We get the length of digits of both x and y
    let n = Math.max(xStr.length, yStr.length);
    xStr = xStr.padStart(n, '0');
    yStr = yStr.padStart(n, '0');

    // Base cases
    if (n == 1) {
        return x * y;
    }
    
    let halfN = Math.floor(n/2);
    
    // Split in half both x and y
    let x_left = parseInt(xStr.substring(0, n - halfN));
    let x_right = parseInt(xStr.substring(n - halfN));

    let y_left = parseInt(yStr.substring(0, n - halfN));
    let y_right = parseInt(yStr.substring(n - halfN));

    let u = x_left + x_right;
    let v = y_left + y_right;

    let a = karatsuba(x_left, y_left);
    let b = karatsuba(x_right, y_right);
    let c = karatsuba(u, v);

    let z = c - a - b;

    return a * Math.pow(10, n) + z * Math.pow(10, halfN) + b
}

console.log(karatsuba(123, 123))