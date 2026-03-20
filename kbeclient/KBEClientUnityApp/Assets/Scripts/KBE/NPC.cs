using UnityEngine;

namespace KBEngine
{
    public class NPC : NPCBase
    {
        private EntityController _entityController;
        private float _objHeight = 0f;
        public override void __init__()
        {
            base.__init__();
            LogMgr.Instance.AddLog($"NPC()");
            Event.registerOut("NPC_OnEnterWorldCallback_"+this.id, this, "OnEnterWorldCallback");
        }

        public override void onDestroy()
        {
            base.onDestroy();
            Event.deregisterOut(this);
        }

        public override void onEnterWorld()
        {
            base.onEnterWorld();
            Event.fireOut("NPC_OnEnterWorldCallback_"+this.id);
        }

        public void OnEnterWorldCallback()
        {
            GameObject npcPrefab = Resources.Load<GameObject>("NPC");
            GameObject npc = Object.Instantiate(npcPrefab);
            _objHeight = npcPrefab.GetComponent<CapsuleCollider>().height ;
            npc.name = "npc_" + id;

            renderObj = npc;


            // 设置头顶信息
            var headInfoUI = npc.GetComponent<HeadInfoUI>();
            headInfoUI.SetName(name);




            _entityController = npc.GetComponent<EntityController>();
            _entityController.entity = this;
            _entityController.moveSpeed = motion.moveSpeed;

            _entityController.SetPosition(new Vector3(-position.x,position.y + (_objHeight / 2),position.z),true);
        }

        public override void onLeaveWorld()
        {
            Object.Destroy((GameObject)renderObj);
        }

        public override void onPositionChanged(KBVector3 oldValue)
        {
            base.onPositionChanged(oldValue);
            if (renderObj != null)
            {
                // ((GameObject)renderObj).transform.position = new Vector3(-position.x,position.y,position.z);
                _entityController.SetPosition(new Vector3(-position.x,position.y+ (_objHeight / 2),position.z),true);
            }
        }

        public override void onSmoothPositionChanged(KBVector3 oldValue)
        {
            base.onSmoothPositionChanged(oldValue);
            if (renderObj != null)
            {
                // ((GameObject)renderObj).transform.position = new Vector3(-position.x,position.y,position.z);
                _entityController.SetPosition(new Vector3(-position.x,position.y+ (_objHeight / 2),position.z),false);
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
    }

}