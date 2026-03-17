using UnityEngine;

namespace KBEngine
{
    public class Avatar : AvatarBase
    {
        public static Avatar Instance;
        public override void __init__()
        {
            base.__init__();
            if (isPlayer()) Instance = this;

            LogMgr.Instance.AddLog($"Avatar()");
            Event.registerOut("Avatar_onEnterSpaceCallback_"+this.id, this, "OnEnterSpaceCallback");
        }


        public override void onDestroy()
        {
            base.onDestroy();
            Event.deregisterOut(this);
        }

        public override void onEnterSpace()
        {
            base.onEnterSpace();
            Event.fireOut("Avatar_onEnterSpaceCallback_"+this.id);
        }

        public override void onLeaveSpace()
        {
            base.onLeaveSpace();
            Object.Destroy((GameObject)renderObj);
        }


        public void OnEnterSpaceCallback()
        {
            GameObject playerPrefab = Resources.Load<GameObject>("Player");
            GameObject player = Object.Instantiate(playerPrefab);
            player.transform.position = this.position;
            player.name = "player_" + id;

            renderObj = player;


            // 设置头顶信息
            var headInfoUI = player.GetComponent<HeadInfoUI>();
            headInfoUI.SetName(name);
            headInfoUI.SetHP(HP,HP_Max);
        }


        public override void onHPChanged(int oldValue)
        {
            base.onHPChanged(oldValue);
            if (renderObj  == null) return;
            var headInfoUI = ((GameObject)renderObj).GetComponent<HeadInfoUI>();
            headInfoUI.SetHP(HP,HP_Max);
        }

        public override void onHP_MaxChanged(int oldValue)
        {
            base.onHP_MaxChanged(oldValue);
            if (renderObj  == null) return;
            var headInfoUI = ((GameObject)renderObj).GetComponent<HeadInfoUI>();
            headInfoUI.SetHP(HP,HP_Max);
        }


        public override void onStateChanged(sbyte oldValue)
        {
            base.onStateChanged(oldValue);
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