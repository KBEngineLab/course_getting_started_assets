namespace KBEngine
{


    public class Account : AccountBase
    {
        public Account()
        {
            LogMgr.Instance.AddLog("Account()");
        }

        public override void __init__()
        {
            base.__init__();
            // Event.fireOut(KBECustomEventTypes.onLoginSuccessfully,id);
            LoginUIEvent.instance.OnLoginSuccessfully(id);
        }

        public override void onReqAvatarList(byte[] arg1)
        {
            throw new System.NotImplementedException();
        }

        public override void onReqCreateAvatar(byte arg1, byte[] arg2)
        {
            throw new System.NotImplementedException();
        }

        public override void onReqRemoveAvatar(byte arg1, long arg2)
        {
            throw new System.NotImplementedException();
        }
    }

}