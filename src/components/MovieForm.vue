<template>
    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control"></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
  
      <div v-if="message" class="alert alert-success">
        {{ message }}
      </div>
      <div v-if="errors.length" class="alert alert-danger">
        <div v-for="error in errors" :key="error">{{ error }}</div>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let csrf_token = ref('');
  let message = ref('');
  let errors = ref([]);
  
  function getCsrfToken() {
    fetch('http://127.0.0.1:8000/api/v1/csrf-token')
      .then(response => response.json())
      .then(data => {
        csrf_token.value = data.csrf_token;
      });
  }
  
 
function saveMovie() {
  let movieForm = document.getElementById('movieForm');
  let formData = new FormData(movieForm);
  fetch('http://127.0.0.1:8000/api/v1/movies', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(response => {
    if (!response.ok) {
      throw response;
    }
    return response.json();
  })
  .then(data => {
    if (data.message) {
      message.value = data.message;
      errors.value = [];
    } else if (data.errors) {
      errors.value = data.errors;
      message.value = '';
    }
  })
  .catch(errorResponse => {
    errorResponse.json().then(errorData => {
      console.error('Error:', errorData);
      if (errorData.error) {
        errors.value = [errorData.error];
      } else {
        errors.value = errorData.errors;
      }
      message.value = '';
    });
  });
}

onMounted(() => {
  getCsrfToken();
});
  </script>
  