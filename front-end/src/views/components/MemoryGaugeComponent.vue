<template>
  <div class="memory-gauge">
    <h2>Memory Usage</h2>
    <GaugeComponent
    :total-size="totalSize"
    :remaining-size="remainingSize"
    :node-name="nodeName" /> <!-- Ensure nodeName is a defined prop on GaugeComponent -->
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import GaugeComponent from "./GaugeComponent.vue";

// Props are defined to accept totalSize and remainingSize from the parent component
const props = defineProps({
  totalSize: Number,
  remainingSize: Number,
  nodeName: String // Ensure this is defined
});

const { totalSize, remainingSize } = props;
</script>
