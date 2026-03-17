using UnityEngine;

namespace KBEngine
{
    public class Monster : MonsterBase
    {
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

        public override void onDestroy()
        {
            base.onDestroy();
            Event.deregisterOut(this);
        }

        public override void __init__()
        {
            base.__init__();
            Event.registerOut("Monster_OnEnterWorldCallback_"+this.id, this, "OnEnterWorldCallback");
        }

        public override void onEnterWorld()
        {
            base.onEnterWorld();
            Event.fireOut("Monster_OnEnterWorldCallback_"+this.id);
        }

        public void OnEnterWorldCallback()
        {
            GameObject monsterPrefab = Resources.Load<GameObject>("Monster");
            GameObject monster = Object.Instantiate(monsterPrefab);
            monster.transform.position = this.position;
            monster.name = "monster_" + id;

            renderObj = monster;


            // 设置头顶信息
            var headInfoUI = monster.GetComponent<HeadInfoUI>();
            headInfoUI.SetName(name);
            headInfoUI.SetHP(HP,HP_Max);
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
                ((GameObject)renderObj).transform.position = new Vector3(-position.x,position.y,position.z);
            }
        }

        public override void onSmoothPositionChanged(KBVector3 oldValue)
        {
            base.onSmoothPositionChanged(oldValue);
            if (renderObj != null)
            {
                ((GameObject)renderObj).transform.position = new Vector3(-position.x,position.y,position.z);
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