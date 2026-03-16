using UnityEngine;

namespace KBEngine
{


    public class Account : AccountBase
    {
        public static Account instance;
        public Account()
        {
            LogMgr.Instance.AddLog("Account()");
        }


        public override void __init__()
        {
            base.__init__();
            if (isPlayer()) instance = this;

            // Event.fireOut(KBECustomEventTypes.onLoginSuccessfully,id);
            LoginUIEvent.instance.OnLoginSuccessfully(id);

        }


        public override void onReqAvatarList(AVATAR_LIST arg1)
        {
            foreach (var avatarInfo in arg1)
            {
                Debug.Log(avatarInfo);
            }
            
        }

        public override void onReqCreateAvatar(byte arg1, AVATAR_LIST arg2)
        {
            if (arg1 == 0)
            {
                LogMgr.Instance.AddLog($"Create Avatar error,recode = {arg1}");
                return;
            }

            if (arg1 == 2)
            {
                LogMgr.Instance.AddLog("Character creation failed, maximum number reached.");
            }

            foreach (var avatarInfo in arg2)
            {
                Debug.Log(avatarInfo);
            }
        }

        public override void onReqRemoveAvatar(byte arg1, long arg2)
        {
            throw new System.NotImplementedException();
        }
    }

}