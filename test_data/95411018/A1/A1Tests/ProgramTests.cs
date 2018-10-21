using Microsoft.VisualStudio.TestTools.UnitTesting;
using TestCommon;

namespace A1.Tests
{
    [TestClass()]
    public class ProgramTests
    {
        [TestMethod()]
        public void AddTest()
        {
            Assert.AreEqual<int>(12, Program.Add(5, 7));
        }

        [TestMethod(), Timeout(1000)]
        [DeploymentItem("TestData", "A1_TestData")]
        public void GradedTest()
        {
            TestTools.RunLocalTest("A1", Program.Process);
        }
    }
}