"""
Fine-tuning API
涵盖: 创建 job / 查询状态 / 列举 jobs / 监听事件 / 取消 / 使用微调模型
注意: 实际微调需要 ≥10 条训练数据且耗时较长（通常数分钟到数小时）
"""
import time
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.client import client


def list_jobs(limit: int = 5):
    print(f"=== 列举最近 {limit} 个 Fine-tuning Jobs ===")
    jobs = client.fine_tuning.jobs.list(limit=limit)
    if not jobs.data:
        print("  暂无 fine-tuning jobs")
        return
    for job in jobs.data:
        print(f"  {job.id}  model={job.model:30s}  status={job.status}")


def create_job(training_file_id: str, validation_file_id: str | None = None):
    """
    Args:
        training_file_id: 已上传的 JSONL 文件 ID (purpose=fine-tune)
        validation_file_id: 可选验证集文件 ID
    """
    print("\n=== 创建 Fine-tuning Job ===")
    kwargs = {
        "training_file": training_file_id,
        "model": "gpt-4o-mini-2024-07-18",
        "hyperparameters": {
            "n_epochs": "auto",
            "batch_size": "auto",
            "learning_rate_multiplier": "auto",
        },
        "suffix": "my-custom-model",
    }
    if validation_file_id:
        kwargs["validation_file"] = validation_file_id

    job = client.fine_tuning.jobs.create(**kwargs)
    print(f"  job_id: {job.id}")
    print(f"  status: {job.status}")
    print(f"  model: {job.model}")
    return job.id


def get_job(job_id: str):
    print(f"\n=== 获取 Job 详情: {job_id} ===")
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"  status: {job.status}")
    print(f"  model: {job.model}")
    print(f"  fine_tuned_model: {job.fine_tuned_model}")
    print(f"  trained_tokens: {job.trained_tokens}")
    if job.error:
        print(f"  ❌ error: {job.error.message}")
    return job


def list_events(job_id: str, limit: int = 10):
    print(f"\n=== Job 事件: {job_id} ===")
    events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=limit)
    for event in reversed(events.data):
        print(f"  [{event.created_at}] {event.message}")


def list_checkpoints(job_id: str):
    print(f"\n=== Job Checkpoints: {job_id} ===")
    checkpoints = client.fine_tuning.jobs.checkpoints.list(job_id)
    if not checkpoints.data:
        print("  暂无 checkpoints")
        return
    for cp in checkpoints.data:
        metrics = cp.metrics
        print(f"  step={cp.step_number}  train_loss={metrics.train_loss:.4f}  model={cp.fine_tuned_model_checkpoint}")


def cancel_job(job_id: str):
    print(f"\n=== 取消 Job: {job_id} ===")
    job = client.fine_tuning.jobs.cancel(job_id)
    print(f"  status: {job.status}")


def wait_for_job(job_id: str, poll_interval: int = 30, timeout: int = 3600):
    """轮询等待 job 完成"""
    print(f"\n=== 等待 Job 完成: {job_id} ===")
    start = time.time()
    while time.time() - start < timeout:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"  [{int(time.time()-start)}s] status: {job.status}")
        if job.status in ("succeeded", "failed", "cancelled"):
            if job.status == "succeeded":
                print(f"  ✅ 微调完成！模型: {job.fine_tuned_model}")
            else:
                print(f"  ❌ 微调{job.status}")
            return job
        time.sleep(poll_interval)
    raise TimeoutError(f"Job 超时（{timeout}s）")


def use_fine_tuned_model(model_id: str, prompt: str = "你好"):
    """
    使用微调后的模型推理
    model_id 形如: ft:gpt-4o-mini-2024-07-18:org:suffix:id
    """
    print(f"\n=== 使用微调模型: {model_id} ===")
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "你是一个简洁准确的知识助手"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
    )
    print(f"  回复: {response.choices[0].message.content}")


if __name__ == "__main__":
    list_jobs()

    # ── 完整流程示例（取消注释并替换 file_id）────────────────────────
    # 步骤1: 先用 files/files_demo.py 上传训练数据，获取 file_id
    # TRAINING_FILE_ID = "file-xxxx"
    # job_id = create_job(TRAINING_FILE_ID)
    # job = wait_for_job(job_id)
    # if job.status == "succeeded":
    #     use_fine_tuned_model(job.fine_tuned_model, "1加1等于几？")
    # ─────────────────────────────────────────────────────────────────
