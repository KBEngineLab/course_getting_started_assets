using UnityEngine;

namespace KBEngine
{
    public class Avatar : AvatarBase
    {
        public static Avatar Instance;
        private EntityController _entityController;
        private PlayerController _playerController;
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
            if (isPlayer())
            {
                Event.fireOut("Avatar_onEnterSpaceCallback_"+this.id);
            }
        }

        public override void onLeaveSpace()
        {
            base.onLeaveSpace();
            Object.Destroy((GameObject)renderObj);
        }


        public void OnEnterSpaceCallback()
        {
            GameObject playerPrefab = Resources.Load<GameObject>(isPlayer() ? "Player":"Avatar");
            GameObject player = Object.Instantiate(
                playerPrefab,
                new Vector3(-position.x, position.y, position.z),
                Quaternion.identity
            );
            player.name = (isPlayer() ? "Player_":"Avatar_") + id;
            renderObj = player;



            // 设置头顶信息
            var headInfoUI = player.GetComponent<HeadInfoUI>();
            headInfoUI.SetName(name);
            headInfoUI.SetHP(HP,HP_Max);


            if (isPlayer())
            {
                _playerController = player.GetComponent<PlayerController>();
                _playerController.moveSpeed = moveSpeed;
                _playerController.avatar = this;
                // player.transform.position = new Vector3(-position.x,position.y,position.z);
                if (WorldUIEvent.Instance)
                {
                    WorldUIEvent.Instance.UpdateReviveBtnState(state);
                }
            }
            else
            {
                _entityController = player.GetComponent<EntityController>();
                _entityController.entity = this;
                _entityController.moveSpeed = moveSpeed;
                _entityController.SetPosition(new Vector3(-position.x,position.y,position.z),true);
            }


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

            if (isPlayer())
            {
                if (WorldUIEvent.Instance)
                {
                    WorldUIEvent.Instance.UpdateReviveBtnState(state);
                }
            }
        }

        // 其他avatar进入到世界时
        public override void onEnterWorld()
        {
            base.onEnterWorld();
            if (!isPlayer())
            {
                Event.fireOut("Avatar_onEnterSpaceCallback_"+this.id);
            }
        }

        public override void onLeaveWorld()
        {
            base.onLeaveWorld();
            Object.Destroy((GameObject)renderObj);
        }

        public override void onPositionChanged(KBVector3 oldValue)
        {
            base.onPositionChanged(oldValue);

            if (isPlayer())
            {
                if (_playerController) _playerController.transform.position = new Vector3(-position.x,position.y,position.z);

            }
            else
            {
                if (_entityController)  _entityController.SetPosition(new Vector3(-position.x,position.y,position.z),true);
            }
        }

        public override void onSmoothPositionChanged(KBVector3 oldValue)
        {
            base.onSmoothPositionChanged(oldValue);
            if (!isPlayer())
            {
                if (_entityController) _entityController.SetPosition(new Vector3(-position.x,position.y,position.z),false);
            }
        }

        public override void onDirectionChanged(KBVector3 oldValue)
        {
            base.onDirectionChanged(oldValue);
            if (renderObj != null)
            {
                ((GameObject)renderObj).transform.rotation = Quaternion.Euler(new Vector3(0, -direction.z, 0));
            }
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