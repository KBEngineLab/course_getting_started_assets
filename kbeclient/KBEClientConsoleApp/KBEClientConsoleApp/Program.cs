
using KBEngine;


bool running = true;
KBELog.Init(new ConsoleLogProvider());

Console.WriteLine("请输入用户名：");
string username = Console.ReadLine();
Console.WriteLine("请输入密码：");
string password = Console.ReadLine();


KBEngineArgs kbeArgs = new KBEngineArgs();

kbeArgs.clientType = KBEngineApp.CLIENT_TYPE.CLIENT_TYPE_MINI;
kbeArgs.ip = "127.0.0.1";
kbeArgs.port = 20013;
kbeArgs.networkType = KBEngineApp.NETWORK_TYPE.KCP;
kbeArgs.isMultiThreads = false;
kbeArgs.useAliasEntityID = true;


KBEngineApp app = new KBEngineApp(kbeArgs);



Thread kbeThread = new Thread(KBELoop);
kbeThread.Start();


app.login(username, password, []);


Console.WriteLine("输入内容，按回车发送，输入exit 退出");

while (running) { 
    string input = Console.ReadLine();

    if (input == null) continue;

    if (input.ToLower() == "exit") {
        running = false;
        break;
    }


    if (FirstEntity.Instance != null) {
        FirstEntity.Instance.cellEntityCall.say(input);
    } else {
        Console.WriteLine("尚未登录或实体未创建，无法发送消息");
    }
}


Console.WriteLine("正在退出...");
app.destroy();
kbeThread.Join();



void KBELoop() { 
    while (running) {
        app.process();
        KBEngine.Event.processOutEvents();
        System.Threading.Thread.Sleep(100);
    }
}