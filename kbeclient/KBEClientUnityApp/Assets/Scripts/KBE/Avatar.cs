namespace KBEngine
{
    public class Avatar : AvatarBase
    {
        public override void __init__()
        {
            base.__init__();
            LogMgr.Instance.AddLog($"Avatar()");
        }

        public override void onDialog(int arg1, string arg2)
        {
            throw new System.NotImplementedException();
        }

        public override void onJump()
        {
            throw new System.NotImplementedException();
        }
    }

}