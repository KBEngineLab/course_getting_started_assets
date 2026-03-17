using UnityEngine;
using UnityEngine.SceneManagement;

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
            LoginUIEvent.Instance.OnLoginSuccessfully(id);

        }


        public override void onEnter(string arg1)
        {
            if (arg1 == "world")
            {
                //暂停所有事件的派发
                LogMgr.Instance.AddLog("Event pause");
                SceneManager.LoadScene("Scenes/World");
                Event.pause();
            }
            else
            {
                LogMgr.Instance.AddLog("Scene does not exist!");
            }
        }

        public override void onReqAvatarList(AVATAR_LIST arg1)
        {
            foreach (var avatarInfo in arg1)
            {
                Debug.Log(avatarInfo);
            }

            LoginUIEvent.Instance.UpdateAvatarList(arg1);
            
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

            LoginUIEvent.Instance.UpdateAvatarList(arg2);
        }

        public override void onReqRemoveAvatar(byte arg1, long arg2)
        {
            if (arg1 == 1)
            {
                LogMgr.Instance.AddLog("Remove avatar success");
                baseEntityCall.reqAvatarList();
            }
            else
            {
                LogMgr.Instance.AddLog("Remove avatar error");
            }

        }
    }

}