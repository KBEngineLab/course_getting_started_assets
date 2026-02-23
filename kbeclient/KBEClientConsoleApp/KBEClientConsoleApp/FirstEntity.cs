using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace KBEngine
{
    public class FirstEntity : FirstEntityBase
    {
        private static FirstEntity _instance;

        public static FirstEntity Instance {
            get {
                return _instance;
            }
        }

        public override void __init__()
        {
            base.__init__();
            if(isPlayer()) _instance = this;


            this.baseEntityCall?.helloBase("Hello from FirstEntity!");
        }

        public override void onDestroy()
        {
            base.onDestroy();
            if(_instance == this) _instance = null;
        }

        public override void onEnter()
        {
             Console.WriteLine("FirstEntity::onEnter");
        }

        public override void onSay(string arg1)
        {
             Console.WriteLine($"FirstEntity::onSay: {arg1}");
        }

    }
}
