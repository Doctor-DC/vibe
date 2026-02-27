<template>
  <div class="modal-overlay">
    <div class="modal">
      <div class="modal-icon">😞</div>
      <h2>游戏失败</h2>
      <p>你出错了太多次！少了解了一些乐队。</p>
      
      <div class="modal-actions">
        <button @click="$emit('retry')" class="btn btn-primary">再试一次</button>
        <button @click="$emit('home')" class="btn btn-secondary">返回首页</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FailureModal'
}
</script>

<style scoped lang="scss">
@import '../../styles/variables';
@import '../../styles/mixins';

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;

  .modal-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  h2 {
    color: color(accent);
    margin-bottom: 0.5rem;
  }

  p {
    color: color(muted);
    margin-bottom: 2rem;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-actions {
  display: flex;
  gap: 1rem;

  .btn {
    flex: 1;
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
  }

  .btn-primary {
    background: color(accent);
    color: white;
  }

  .btn-secondary {
    background: color(light-white-04);
    color: color(text);
  }
}
</style>
