using UnityEngine;

public class EntityController : MonoBehaviour
{
    public KBEngine.Entity entity;

    private Vector3 targetPos;

    public float moveSpeed = 5f;

    void Start()
    {
        targetPos = transform.position;
    }

    void Update()
    {
        SmoothMove();
    }

    /// <summary>
    /// 设置位置
    /// </summary>
    /// <param name="pos">目标位置</param>
    /// <param name="isTeleport">是否瞬移</param>
    public void SetPosition(Vector3 pos, bool isTeleport = false)
    {
        if (isTeleport)
        {
            // 直接瞬移
            transform.position = pos;
            targetPos = pos;
        }
        else
        {
            // 正常平滑移动
            targetPos = pos;
        }
    }

    void SmoothMove()
    {
        transform.position = Vector3.MoveTowards(
            transform.position,
            targetPos,
            moveSpeed * Time.deltaTime
        );
    }
}