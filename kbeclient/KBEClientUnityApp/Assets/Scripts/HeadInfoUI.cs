using UnityEngine;
using TMPro;
using System.Collections.Generic;

public class HeadInfoUI : MonoBehaviour
{
    // ====== 全局 Canvas（所有玩家共用） ======
    private static Canvas worldCanvas;
    private static Transform cam;

    // ====== 当前对象UI ======
    private RectTransform root;
    private TextMeshProUGUI nameText;
    private TextMeshProUGUI hpText;

    private Vector3 offset = new Vector3(0, 2f, 0);

    // ====== 数据 ======
    public string playerName;
    public int hp;
    public int maxHp;

    public bool showHp;

    // ====== 初始化 ======
    void Start()
    {
        InitCanvas();
        CreateUI();
        UpdateUI();
    }

    // ====== 创建全局Canvas（只创建一次） ======
    void InitCanvas()
    {
        if (worldCanvas != null) return;

        GameObject canvasObj = new GameObject("WorldCanvas");
        worldCanvas = canvasObj.AddComponent<Canvas>();
        worldCanvas.renderMode = RenderMode.WorldSpace;

        canvasObj.AddComponent<UnityEngine.UI.CanvasScaler>();
        canvasObj.AddComponent<UnityEngine.UI.GraphicRaycaster>();

        RectTransform rect = worldCanvas.GetComponent<RectTransform>();
        rect.sizeDelta = new Vector2(1920, 1080);
        // Unity UI 的单位是“像素”，但 3D 世界单位是“米” ,所以这里需要缩放
        rect.localScale = Vector3.one * 0.01f;

        if (Camera.main != null)
            cam = Camera.main.transform;
        else
            cam = FindObjectOfType<Camera>().transform;
    }

    // ====== 创建UI ======
    void CreateUI()
    {
        GameObject rootObj = new GameObject("HeadInfo");
        // SetParent 默认“保持世界变换” → 导致 scale 被改成 100,设置为false
        rootObj.transform.SetParent(worldCanvas.transform,false);

        root = rootObj.AddComponent<RectTransform>();
        root.sizeDelta = new Vector2(200, 100);

        // ===== Name =====
        GameObject nameObj = new GameObject("Name");
        nameObj.transform.SetParent(root,false);

        nameText = nameObj.AddComponent<TextMeshProUGUI>();
        nameText.alignment = TextAlignmentOptions.Center;
        nameText.fontSize = 32;

        RectTransform nameRect = nameText.GetComponent<RectTransform>();
        nameRect.anchorMin = new Vector2(0, 0.5f);
        nameRect.anchorMax = new Vector2(1, 1);
        nameRect.offsetMin = Vector2.zero;
        nameRect.offsetMax = Vector2.zero;

        if (showHp)
        {
            // ===== HP =====
            GameObject hpObj = new GameObject("HP");
            hpObj.transform.SetParent(root,false);

            hpText = hpObj.AddComponent<TextMeshProUGUI>();
            hpText.alignment = TextAlignmentOptions.Center;
            hpText.fontSize = 28;

            RectTransform hpRect = hpText.GetComponent<RectTransform>();
            hpRect.anchorMin = new Vector2(0, 0);
            hpRect.anchorMax = new Vector2(1, 0.5f);
            hpRect.offsetMin = Vector2.zero;
            hpRect.offsetMax = Vector2.zero;
        }

    }

    // ====== 每帧更新位置 + 朝向 ======
    void LateUpdate()
    {
        if (root == null || cam == null) return;

        // 跟随头顶
        root.position = transform.position + offset;

        // 朝向相机
        root.forward = cam.forward;
    }

    // ====== 对外初始化 ======
    public void Init(string name, int hp, int maxHp)
    {
        this.playerName = name;
        this.hp = hp;
        this.maxHp = maxHp;

        UpdateUI();
    }

    // ====== 更新血量 ======
    public void SetHP(int value)
    {
        hp = Mathf.Clamp(value, 0, maxHp);
        UpdateUI();
    }

    public void SetHP(int value,int maxHp)
    {
        hp = Mathf.Clamp(value, 0, maxHp);
        this.maxHp = maxHp;
        UpdateUI();
    }

    // ====== 更新名字 ======
    public void SetName(string name)
    {
        playerName = name;
        UpdateUI();
    }

    // ====== 刷新UI ======
    void UpdateUI()
    {
        if (nameText != null)
            nameText.text = playerName;

        if (hpText != null)
            hpText.text = $"{hp} / {maxHp}";
    }

    // ====== 销毁时清理 ======
    void OnDestroy()
    {
        if (root != null)
        {
            Destroy(root.gameObject);
        }
    }
}