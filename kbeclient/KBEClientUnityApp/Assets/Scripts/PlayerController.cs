using System;
using System.Collections;
using System.Collections.Generic;
using KBEngine;
using UnityEngine;

// 强制要求该物体必须挂载 CharacterController 组件
// 如果没有，Unity 会自动添加
[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    public KBEngine.Avatar avatar;

    // 移动速度（单位：米/秒）
    public float moveSpeed = 5f;

    // 重力加速度（负值表示向下）
    public float gravity = -9.8f;

    // 跳跃高度（单位：米）
    public float jumpHeight = 2f;

    // CharacterController 组件引用
    private CharacterController controller;

    // 当前角色的速度（主要用于处理垂直方向：跳跃 + 重力）
    private Vector3 velocity;

    public LayerMask attackLayer; // 限制可攻击层

    void Start()
    {
        // 获取当前物体上的 CharacterController 组件
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        PlayerMove();
        PlayerAttack();
    }

    void PlayerAttack()
    {
        if (Input.GetMouseButtonDown(0)) // 鼠标左键
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            // 发射射线
            if (Physics.Raycast(ray, out hit, 100f, attackLayer))
            {
                // GameObject target = hit.collider.gameObject;
                EntityController monster = hit.collider.GetComponentInParent<EntityController>();

                if (monster)
                {
                    // 计算距离
                    float distance = Vector3.Distance(transform.position, monster.transform.position);
                    Debug.Log(distance);
                    if (distance <= 8f)
                    {
                        // avatar.cellEntityCall.
                        Debug.Log(monster);
                    }
                    else
                    {
                        Debug.Log("目标太远");
                    }
                }
                else
                {
                    Debug.Log("1111111");
                }

            }
        }
    }

    void PlayerMove()
    {
        if (avatar == null) return;
        // 死亡状态
        if (avatar.state == 1) return;

        // 获取输入
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        // 方向（基于角色朝向）
        Vector3 move = transform.right * h + transform.forward * v;

        // ===== 地面检测 & 贴地 =====
        if (controller.isGrounded && velocity.y < 0)
        {
            // 轻微向下，保证贴地稳定
            velocity.y = -2f;
        }

        // ===== 跳跃 =====
        if (Input.GetKeyDown(KeyCode.Space) && controller.isGrounded)
        {
            // 起跳速度
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
        }

        // ===== 重力 =====
        velocity.y += gravity * Time.deltaTime;

        // ===== 合并移动=====
        Vector3 finalMove = move * moveSpeed + velocity;

        // 只调用一次 Move
        controller.Move(finalMove * Time.deltaTime);

        avatar.position = new KBVector3(-gameObject.transform.position.x,
            gameObject.transform.position.y, gameObject.transform.position.z);
    }
}
