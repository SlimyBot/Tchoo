<template>
  <div class="gears-container">
    <div class="gear-rotate" />
  </div>
</template>
  
  <style scoped>
  * {
    font-family: "Rubik Mono One", sans-serif;
    color: var(--text-color);
  }
  
  /*
  ********************************************************************************************************
  ********************************************************************************************************
  css du menu
  ********************************************************************************************************
  ********************************************************************************************************
  */
  
  .divHeader {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 98%;
    position: absolute;
    margin-bottom: 500px;
  }
  
  .headerTcho {
    font-size: 2em;
  }
  
  .buttonHeader {
    background-color: var(--CTA-2-color);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
  }
  
  .buttonHeader:hover {
    background-color: var(--CTA-color);
    transition: 700ms;
    width: 70px;
    height: 70px;
  }
  
  /*
  ********************************************************************************************************
  ********************************************************************************************************
  css responsive
  ********************************************************************************************************
  ********************************************************************************************************
  */
  
  @media screen and (max-width: 800px) {
    .divHeader {
      width: 90%;
    }
  }
  </style>
  