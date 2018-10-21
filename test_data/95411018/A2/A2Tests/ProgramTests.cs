using Microsoft.VisualStudio.TestTools.UnitTesting;
using A2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TestCommon;

namespace A2.Tests
{
    [TestClass()]
    public class ProgramTests
    {
        [TestMethod()]
        public void GradedTest_Correctness()
        {
            var testData = new List<int>() { 10, 14, 15, 9 };
            var expected = 14 * 15;
            Assert.AreEqual(expected, Program.MaxPairwiseProductNaive(testData));
            Assert.AreEqual(expected, Program.MaxPairwiseProductFast(testData));
        }

        [TestMethod(), Timeout(500)]
        [DeploymentItem("TestData", "A2_TestData")]
        public void GradedTest_Performance()
        {
            TestTools.RunLocalTest("A2", Program.Process);
        }

        [TestMethod()]
        public void GradedTest_Stress()
        {
            var rnd = new Random();
            var numOfRun = rnd.Next(20, 100);
            for (int i=0; i<numOfRun; ++i)
            {
                var data = DataGenerator();
                Assert.AreEqual(Program.MaxPairwiseProductNaive(data), Program.MaxPairwiseProductFast(data));
            }
        }

        private static List<int> DataGenerator()
        {
            var rnd = new Random();
            var len = rnd.Next(20, 100);
            var data = new List<int>();
            for (int j = 0; j < len; ++j)
            {
                data.Add(rnd.Next(1, 100));
            }
            return data;
        }
    }
}