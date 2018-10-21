using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace A2
{
    public class Program
    {
        static void Main(string[] args)
        {
            List<int> testData = new List<int> { 1, 32, 23, 6, 15, 21, 17 };
            MaxPairwiseProductNaive(testData);
        }

        public static int MaxPairwiseProductNaive(List<int> data)
        {
            int prod = int.MinValue;
            for (int i=0; i < data.Count; ++i)
                for (int j=0; j < data.Count; ++j)
                    if (i != j && prod < data[i] * data[j])
                        prod = data[i] * data[j];
            return prod;
        }

        public static int MaxPairwiseProductFast(List<int> data)
        {
            int max1 = int.MinValue;
            int max2 = int.MinValue;
            foreach (int value in data)
                if (value > max1)
                    max1 = value;
            data.Remove(max1);
            foreach (int value in data)
                if (value > max2)
                    max2 = value;
            return max1 * max2;
        }

        public static string Process(string input)
        {
            var inData = input.Split(new char[] { '\n', '\r', ' ' },
                StringSplitOptions.RemoveEmptyEntries)
                .Select(s => int.Parse(s))
                .ToList();
            return MaxPairwiseProductFast(inData).ToString();
        }
    }
}
