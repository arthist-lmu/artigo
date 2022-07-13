<template>
  <div class="stage">
    <div class="waiter"></div>
  </div>
</template>

<style scoped>
.stage {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 2px 0;
  overflow: hidden;
}

.waiter {
  position: relative;
  left: -9999px;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #424798;
  color: #424798;
  box-shadow: 9999px 0 0 -5px #424798;
  animation: waiter 1.5s infinite linear;
  animation-delay: .25s;
}

.waiter::before,
.waiter::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
  width: 10px;
  height: 10px;
  border-radius: 5px;
  background-color: #424798;
  color: #424798;
}

.waiter::before {
  box-shadow: 9984px 0 0 -5px #424798;
  animation: waiterBefore 1.5s infinite linear;
  animation-delay: 0s;
}

.waiter::after {
  box-shadow: 10014px 0 0 -5px #424798;
  animation: waiterAfter 1.5s infinite linear;
  animation-delay: .5s;
}

@keyframes waiterBefore {
  0% {
    box-shadow: 9984px 0 0 -5px #424798;
  }
  30% {
    box-shadow: 9984px 0 0 2px #424798;
  }
  60%,
  100% {
    box-shadow: 9984px 0 0 -5px #424798;
  }
}

@keyframes waiter {
  0% {
    box-shadow: 9999px 0 0 -5px #424798;
  }
  30% {
    box-shadow: 9999px 0 0 2px #424798;
  }
  60%,
  100% {
    box-shadow: 9999px 0 0 -5px #424798;
  }
}

@keyframes waiterAfter {
  0% {
    box-shadow: 10014px 0 0 -5px #424798;
  }
  30% {
    box-shadow: 10014px 0 0 2px #424798;
  }
  60%,
  100% {
    box-shadow: 10014px 0 0 -5px #424798;
  }
}
</style>
