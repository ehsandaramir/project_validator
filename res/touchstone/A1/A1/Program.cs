using System.IO;
using System.Text;

namespace A1
{
    public class Program
    {
        static void Main(string[] args)
        {
        }

        public static int Add(int a, int b)
        {
            return a + b;
        }

        public static string Process(string input)
        {
            StringBuilder sb = new StringBuilder();
            using (StringReader reader = new StringReader(input))
            using (StringWriter writer = new StringWriter(sb))
            {
                int a = int.Parse(reader.ReadLine());
                int b = int.Parse(reader.ReadLine());
                writer.WriteLine(Add(a, b));
            }
            return sb.ToString();
        }

    }
}
