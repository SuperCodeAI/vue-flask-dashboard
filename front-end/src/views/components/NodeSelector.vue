<template>
  <div class="node-selector-container">
    <!-- Header above the entire container -->
    <div class="node-header">
      <h2>Node Selection</h2>
    </div>
    <!-- Main content area for node selection -->
    <div class="node-content">
      <!-- Node list on the far left -->
      <div class="node-list">
        <ul>
          <li
            v-for="node in nodes"
            :key="node.id"
            @click="toggleNodeSelection(node)"
            :class="{ selected: isSelected(node) }"
          >
            {{ node.name }}
          </li>
        </ul>
      </div>

      <!-- Description of the selected node in the middle -->
      <div class="node-description" v-if="selectedNode">
        <h3>{{ selectedNode.name }} Description</h3>
        <p>{{ selectedNode.description }}</p>
      </div>
      <div class="node-description" v-else>
        <p>Select a node to see its description.</p>
      </div>

      <!-- List of selected nodes on the far right -->
      <div class="selected-nodes">
        <h3>Selected Nodes</h3>
        <ul>
          <li v-for="node in modelValue" :key="node.id">
            {{ node.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: Array,
});
const emit = defineEmits(["update:modelValue"]);

const nodes = ref([
  {
    id: 1,
    name: "Node 1",
    description: "Description of Node 1",
    selected: false,
  },
  {
    id: 2,
    name: "Node 2",
    description: "Description of Node 2",
    selected: false,
  },
  {
    id: 3,
    name: "Node 3",
    description: "Description of Node 3",
    selected: false,
  },
  {
    id: 4,
    name: "Node 4",
    description: "Description of Node 4",
    selected: false,
  },
  {
    id: 5,
    name: "Node 5",
    description: "Description of Node 5",
    selected: false,
  },
  {
    id: 6,
    name: "Node 6",
    description: "Description of Node 6",
    selected: false,
  },
  {
    id: 7,
    name: "Node 7",
    description: "Description of Node 7",
    selected: false,
  },
  {
    id: 8,
    name: "Node 8",
    description: "Description of Node 8",
    selected: false,
  },
  {
    id: 9,
    name: "Node 9",
    description: "Description of Node 9",
    selected: false,
  },
  // Add more nodes as needed
]);

const selectedNode = ref(null);
const isSelected = (node) =>
  props.modelValue.some((selectedNode) => selectedNode.id === node.id);

const toggleNodeSelection = (node) => {
  const index = props.modelValue.findIndex(
    (selectedNode) => selectedNode.id === node.id,
  );
  if (index === -1) {
    emit("update:modelValue", [...props.modelValue, node]);
  } else {
    const newSelection = [...props.modelValue];
    newSelection.splice(index, 1);
    emit("update:modelValue", newSelection);
  }
  selectedNode.value = node;
};
</script>

<style scoped>
.node-selector-container {
  display: flex;
  flex-direction: column;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 8px;
}

.node-header {
  padding: 10px 20px;
  background-color: #f5f5f5;
  text-align: left;
  font-size: 1.25rem;
  border-bottom: 1px solid #ddd;
}

.node-content {
  display: flex;
}

.node-list,
.node-description,
.selected-nodes {
  padding: 20px;
  flex-basis: 33.3333%;
  flex-grow: 1;
  border-right: 1px solid #ddd;
}

.node-list ul,
.selected-nodes ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.node-list li,
.selected-nodes li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.node-list li:hover,
.node-list li.selected,
.selected-nodes li:hover {
  background-color: #b1f397;
}

/* Remove border from the last element of the main content */
.selected-nodes {
  border-right: none;
}

/* Optional: Add some responsive styling */
@media (max-width: 768px) {
  .node-content {
    flex-direction: column;
  }

  .node-list,
  .node-description,
  .selected-nodes {
    border-right: none;
    border-bottom: 1px solid #ddd;
    flex-basis: auto;
  }

  .selected-nodes {
    border-bottom: none;
  }
}
</style>
