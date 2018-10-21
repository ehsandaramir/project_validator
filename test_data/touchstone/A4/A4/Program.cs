using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TestCommon;

namespace A4
{
    public class Program
    {
        static void Main(string[] args)
        {
        }

        private static int[] coins = new int[] { 10, 5, 1 };

        public static long ChangingMoney1(long money)
        {
            int num = 0;
            while ( money > 0)
            {
                num += 1;
                var tmp = 0;
                foreach (var coin in coins)
                {
                    if (coin <= money)
                    {
                        money -= coin;
                        break;
                    }
                }
            }
            return num;
        }

        private static int PopMax(List<double> values)
        {
            double val = values[0];
            int index = 0;
            for(int i=1; i<values.Count; ++i)
            {
                if (val < values[i])
                {
                    val = values[i];
                    index = i;
                }
            }
            values[index] = 0;
            return index;
        }

        public static long MaximizingLoot2(long capacity, long[] weights, long[] values)
        {
            var density = new List<double>();
            for(int i=0; i<weights.Length; ++i)
            {
                density.Add(values[i] / (double)weights[i]);
            }
            double total = 0;
            double cap = capacity;
            while (cap > 0)
            {
                var index = PopMax(density);
                if (cap >= weights[index])
                {
                    cap -= weights[index];
                    total += values[index];
                }
                else
                {
                    total += (cap / weights[index]) * values[index];
                    cap = 0;
                }
            }
            return (long)(total);
        }

        public static long MaximizingOnlineAdRevenue3(long slotCount, long[] adRevenue, long[] averageDailyClick)
        {
            Array.Sort(adRevenue);
            Array.Sort(averageDailyClick);
            long total = 0;
            for(long i=0; i<slotCount; ++i)
                total += (adRevenue[i] * averageDailyClick[i]);
            return total;
        }

        private class Span : IComparable<Span>
        {
            public Span(long st, long sp)
            {
                start = st;
                stop = sp;
            }

            public long start = long.MinValue;
            public long stop = long.MinValue;

            public int CompareTo(Span other)
            {
                return - other.start.CompareTo(start);
            }
        }

        public static long CollectingSignatures4(long count, long[] startTime, long[] endTime)
        {
            var spans = new List<Span>();
            for (int i=0; i<count; ++i)
                spans.Add( new Span(startTime[i], endTime[i]) );

            spans.Sort();
            long total = 0;
            while (spans.Count > 0)
            {
                var endSpan = spans[0].stop;
                total += 1;
                while (spans.Count != 0 && spans[0].start <= endSpan)
                {
                    spans.RemoveAt(0);
                }
            }
            return total;
        }

        public static long[] MaximizeNumberOfPrizePlaces5(long n)
        {
            var dist = new List<long>();

            while (n > dist.Count)
            {
                dist.Add(dist.Count + 1);
                n -= dist.Count;
            }
            dist[dist.Count - 1] += n;
            return dist.ToArray();
        }

        private class Slug : IComparable<Slug>
        {
            public long Value;
            public string ValueStr;

            public Slug(long val)
            {
                Value = val;
                ValueStr = val.ToString();
            }

            public int CompareTo(Slug other)
            {
                string ab = ValueStr + other.ValueStr;
                string ba = other.ValueStr + ValueStr;
                return (ab.CompareTo(ba) > 0 ? -1 : 1);
            }

            public override string ToString()
            {
                return $"Slug<{Value}>";
            }
        }

        public static string MaximizeSalary6(long n, long[] numbers)
        {
            var nums = new List<Slug>();
            foreach (var num in numbers)
                nums.Add(new Slug(num));
            nums.Sort();

            string result = "";
            foreach (Slug tmp in nums)
                result += tmp.ValueStr;
            return result;
        }


        public static string ProcessChangingMoney1(string inStr)
            => TestTools.Process(inStr, (Func<long, long>)ChangingMoney1);

        public static string ProcessMaximizingLoot2(string inStr)
            => TestTools.Process(inStr, (Func<long, long[], long[], long>)MaximizingLoot2);

        public static string ProcessMaximizingOnlineAdRevenue3(string inStr)
            => TestTools.Process(inStr, (Func<long, long[], long[], long>)MaximizingOnlineAdRevenue3);

        public static string ProcessCollectingSignatures4(string inStr)
            => TestTools.Process(inStr, (Func<long, long[], long[], long>)CollectingSignatures4);

        public static string ProcessMaximizeNumberOfPrizePlaces5(string inStr)
            => TestTools.Process(inStr, (Func<long, long[]>)MaximizeNumberOfPrizePlaces5);

        public static string ProcessMaximizeSalary6(string inStr)
            => TestTools.Process(inStr, (Func<long, long[], string>)MaximizeSalary6);
    }
}
