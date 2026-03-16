using UnityEngine;

public class MMOCameraController : MonoBehaviour
{
    [Header("References")]
    public Transform cameraPivot;
    public Transform mainCamera;

    [Header("Rotation")]
    public float mouseSensitivity = 3.5f;
    public float minPitch = -40f;
    public float maxPitch = 70f;

    [Header("Camera Collision")]
    public float defaultDistance = 4f;     // 正常摄像机距离
    public float minDistance = 1.2f;        // 最近距离
    public float collisionRadius = 0.2f;    // SphereCast 半径
    public float zoomSmoothSpeed = 12f;     // 拉近/拉远速度
    public LayerMask collisionMask;         // 地形/建筑层

    private float yaw;
    private float pitch;
    private float currentDistance;

    void Start()
    {
        yaw = transform.eulerAngles.y;

        pitch = cameraPivot.localEulerAngles.x;
        if (pitch > 180) pitch -= 360;

        currentDistance = defaultDistance;
    }

    void Update()
    {
        HandleRotation();
        HandleCameraCollision();
    }

    void HandleRotation()
    {
        if (!Input.GetMouseButton(1))
            return;

        float mouseX = Input.GetAxis("Mouse X");
        float mouseY = Input.GetAxis("Mouse Y");

        yaw += mouseX * mouseSensitivity;
        pitch -= mouseY * mouseSensitivity;
        pitch = Mathf.Clamp(pitch, minPitch, maxPitch);

        // Player 只控制 Y 轴
        transform.rotation = Quaternion.Euler(0f, yaw, 0f);

        // 上下视角
        cameraPivot.localRotation = Quaternion.Euler(pitch, 0f, 0f);
    }

    void HandleCameraCollision()
    {
        Vector3 pivotPos = cameraPivot.position;
        Vector3 camDir = -cameraPivot.forward;

        float targetDistance = defaultDistance;

        // 球形射线，防止贴边抖动
        if (Physics.SphereCast(
            pivotPos,
            collisionRadius,
            camDir,
            out RaycastHit hit,
            defaultDistance,
            collisionMask,
            QueryTriggerInteraction.Ignore))
        {
            targetDistance = Mathf.Clamp(
                hit.distance,
                minDistance,
                defaultDistance
            );
        }

        currentDistance = Mathf.Lerp(
            currentDistance,
            targetDistance,
            Time.deltaTime * zoomSmoothSpeed
        );

        mainCamera.localPosition = new Vector3(0f, 0f, -currentDistance);
    }
}
