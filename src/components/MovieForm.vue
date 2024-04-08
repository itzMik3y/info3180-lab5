<script setup>
import { ref } from "vue";


</script>

<template>
    <div class="container">
      <form class="movie-form">
        <div>
            <label for="title">Title</label>
            <input type="text" name="" id="">
        </div>
        <div>
            <label for="description">Description</label>
            <textarea name="" id="" cols="30" rows="10"></textarea>
        </div>
        <div>

        </div>
      </form>
    </div>
</template>

<style>
.movie-form{
    width: 80vw;
    height: 80vh;
    border: 1px solid black;
}
.movie-form div{
    display: flex;
}
/* Add any component specific styles here */
</style>