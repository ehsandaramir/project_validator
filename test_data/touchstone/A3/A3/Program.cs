using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace A3
{
    public class Program
    {
        private static List<string> _cacheFib = new List<string>() { "0", "1", "1" };
        private static List<int> _cacheFibLast = new List<int>() { 0, 1, 1 };

        public static void Main(string[] args) {
            var tmp = Fibonacci_Partial_Sum(150482468097531, 479);
            Console.WriteLine($"Result: {tmp}");
            Console.ReadKey();
        }

        public static long Fibonacci(long index)
        {
            while (_cacheFib.Count <= index) {
                var value = long.Parse(_cacheFib[_cacheFib.Count - 1]) + long.Parse(_cacheFib[_cacheFib.Count - 2]);
                _cacheFib.Add(value.ToString());
            }
            return long.Parse(_cacheFib[(int) index]);
        }

        public static long Fibonacci_LastDigit(long n)
        {
            while (_cacheFibLast.Count <= n)
            {
                var value = _cacheFibLast[_cacheFibLast.Count - 1] + _cacheFibLast[_cacheFibLast.Count - 2];
                value %= 10;
                _cacheFibLast.Add((int) value);
            }
            return _cacheFibLast[(int) n];
        }

        public static long Fibonacci_LastDigit_CacheLess(long n)
        {
            long first = 0;
            long second = 1;
            long res = 0;
            for (long i=2; i<=n; ++i)
            {
                res = first + second;
                first = second;
                second = res % 10;
            }
            return res % 10;
        }

        public static long GCD(long a, long b)
        {
            long small = 0, big = 0;
            if (a > b)
            {
                small = b;
                big = a;
            }
            else
            {
                small = a;
                big = b;
            }

            if (big % small == 0)
                return small;

            return GCD(small, big % small);
        }

        public static long LCM(long a, long b)
        {
            return (a * b) / GCD(a, b);
        }

        public static long GetPisanoPeriod(long m)
        {
            long a = 0, b = 1, c = a + b;
            for (int i = 0; i < m * m; i++)
            {
                c = (a + b) % m;
                a = b;
                b = c;
                if (a == 0 && b == 1) return i + 1;
            }
            return 0;
        }

        public static long Fibonacci_Mod(long n, long m)
        {
            long remainder = n % GetPisanoPeriod(m);

            long first = 0;
            long second = 1;

            long res = remainder;

            for (int i = 1; i < remainder; i++)
            {
                res = (first + second) % m;
                first = second;
                second = res;
            }

            return res % m;
        }


        public static long Fibonacci_Sum(long n)
        {
            n = (n + 2) % 60;
            int[] fib = new int[n + 2];
            fib[0] = 0;
            fib[1] = 1;
            for (int i = 2; i <= n; i++)
            {
                fib[i] = (fib[i - 1] % 10 + fib[i - 2] % 10) % 10;
            }
            if (fib[n] == 0)
            {
                return 9;
            }
            return (fib[n] % 10 - 1);
        }
        
        public static long Fibonacci_Partial_Sum(long n, long m)
        {
            if (m > n)
            {
                var swapVariable = m;
                m = n;
                n = swapVariable;
            }
            var tmp = Fibonacci_Sum(n) - Fibonacci_Sum(m-1);
            if (tmp < 0)
                tmp += 10;
            return tmp;
            //return (Fibonacci_Sum(n) + 10 - Fibonacci_Sum(m - 1)) % 10;
        }

        public static long Fibonacci_Sum_Squares(long n)
        {
            var a = Fibonacci_Mod(n, 10);
            var b = (a + Fibonacci_Mod(n - 1, 10));
            return (a * b) % 10;
        }

        public static string ProcessFibonacci(string arg)
            => Process(arg, Fibonacci);

        public static string ProcessFibonacci_LastDigit(string arg)
            => Process(arg, Fibonacci_LastDigit);

        public static string ProcessFibonacci_LastDigit_CacheLess(string arg)
            => Process(arg, Fibonacci_LastDigit_CacheLess);

        public static string ProcessGCD(string arg)
            => Process(arg, GCD);

        public static string ProcessLCM(string arg)
            => Process(arg, LCM);

        public static string ProcessFibonacci_Mod(string arg)
            => Process(arg, Fibonacci_Mod);

        public static string ProcessFibonacci_Sum(string arg)
            => Process(arg, Fibonacci_Sum);

        public static string ProcessFibonacci_Partial_Sum(string arg)
            => Process(arg, Fibonacci_Partial_Sum);

        public static string ProcessFibonacci_Sum_Squares(string arg)
            => Process(arg, Fibonacci_Sum_Squares);

        public static string Process(string inStr, Func<long, long> longProcessor)
            => longProcessor( long.Parse(inStr) ).ToString();

        public static string Process(string inStr, Func<long, long, long> longProcessor)
        {
            var tokens = inStr.Split(new char[] { '\n', '\r', ' ' }, StringSplitOptions.RemoveEmptyEntries);
            return longProcessor(
                long.Parse(tokens[0]), long.Parse(tokens[1]))
                .ToString();
        }
    }
}
