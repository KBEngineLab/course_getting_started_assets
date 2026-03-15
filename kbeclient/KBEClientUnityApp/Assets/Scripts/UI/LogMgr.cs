using TMPro;
using UnityEngine;

public class LogMgr : MonoBehaviour
{
    private static LogMgr instance;

    public static LogMgr Instance
    {
        get
        {
            if (instance == null)
            {
                // 先尝试在场景里找
                instance = FindObjectOfType<LogMgr>();

                if (instance == null)
                {
                    // 从 Resources 加载预制体
                    GameObject prefab = Resources.Load<GameObject>("LogCanvas");

                    if (prefab != null)
                    {
                        GameObject go = Instantiate(prefab);
                        instance = go.GetComponent<LogMgr>();
                    }
                    else
                    {
                        Debug.LogError("LogCanvas prefab not found in Resources!");
                    }
                }

                if (instance != null)
                {
                    DontDestroyOnLoad(instance.gameObject);
                }
            }

            return instance;
        }
    }

    public Transform content;
    private const int MAX_LOG = 50;

    void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        DontDestroyOnLoad(gameObject);

        ClearLogs();
    }

    void ClearLogs()
    {
        for (int i = content.childCount - 1; i >= 0; i--)
        {
            Destroy(content.GetChild(i).gameObject);
        }
    }

    public void AddLog(string msg)
    {
        if (content.childCount >= MAX_LOG)
        {
            Destroy(content.GetChild(0).gameObject);
        }

        GameObject go = new GameObject("log");
        go.transform.SetParent(content, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        msg = $"[{System.DateTime.Now:HH:mm:ss}] {msg}";
        text.text = msg;
        text.fontSize = 16;
        text.color = Color.white;
        text.enableWordWrapping = false;

        RectTransform rect = text.rectTransform;
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(1, 1);
        rect.pivot = new Vector2(0.5f, 1);
        rect.sizeDelta = new Vector2(0, 0);
    }
}
