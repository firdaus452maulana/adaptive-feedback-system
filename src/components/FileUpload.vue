<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['file-uploaded'])
const fileInput = ref<HTMLInputElement | null>(null)
const uploadStatus = ref('')
const isUploading = ref(false)

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const file = input.files[0]
  isUploading.value = true
  uploadStatus.value = 'Uploading...'

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('Upload failed')

    const result = await response.json()
    uploadStatus.value = 'Upload successful!'
    emit('file-uploaded', result)
  } catch (error) {
    uploadStatus.value = 'Upload failed. Please try again.'
    console.error('Upload error:', error)
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="file-upload">
    <div class="upload-container">
      <input
        type="file"
        ref="fileInput"
        @change="handleFileUpload"
        accept=".json"
        class="form-control"
      >
      <p v-if="uploadStatus" :class="['status-message', { 'error': uploadStatus.includes('failed') }]">
        {{ uploadStatus }}
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.file-upload {
  margin: 2rem 0;
  
  .upload-container {
    border: 2px dashed #B1C29E;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    background-color: #FCE7C8;
  }

  .status-message {
    margin-top: 1rem;
    font-weight: 500;
    
    &.error {
      color: #dc3545;
    }
  }
}
</style>