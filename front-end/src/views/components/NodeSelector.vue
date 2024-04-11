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
    :class="{ 'selected': isNodeSelected(node) }"
  >
    {{ node.name }}
  </li>
        </ul>
      </div>

      <div class="node-description" v-if="selectedNode">
        <h4>{{ selectedNode.name }} 설명</h4>
        <!-- Display additional node details -->
        <p>CPU Core Count: {{ selectedNode.cpu_count }}</p>
        <p>Total Memory: {{ selectedNode.total_memory }} MB</p>
        <p>Total Disk: {{ selectedNode.total_disk }} MB</p>
        <p>Status: {{ nodeStatusDescription }}</p>
      </div>
      <div class="node-description" v-else>
        <p>Select a node to see its description.</p>
      </div>

      <!-- List of selected nodes on the far right -->
      <div class="selected-nodes">
        <h3>Selected Nodes</h3>
        <ul>
          <li v-for="node in sortedSelectedNodes" :key="node.id">
            {{ node.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed, onMounted } from "vue";
import { useStore } from "vuex";

const store = useStore();
const nodes = computed(() => store.getters.userNodes || []);

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [], // Provide a default empty array
  },
});

const isNodeSelected = (node) => {
  // Ensure props.modelValue is an array before calling .some()
  return Array.isArray(props.modelValue) && props.modelValue.some(selectedNode => selectedNode.id === node.id);
};

const emit = defineEmits(["update:modelValue"]);

onMounted(async () => {
  await store.dispatch("fetchNodes"); // 노드 정보 가져와서 마운트하기.
});

const selectedNode = ref(null);
// const isSelected = (node) => {
//   return selectedNode.value && node.id === selectedNode.value.id;
// };

const toggleNodeSelection = (node) => {
  if (node.status !== 0) {
    console.log("Node is not in a waiting state and cannot be selected.");
    return;
  }

  const newSelectedNodes = props.modelValue.includes(node)
    ? props.modelValue.filter(selectedNode => selectedNode.id !== node.id) // Remove node from selection
    : [...props.modelValue, node]; // Add node to selection

  emit("update:modelValue", newSelectedNodes);

  // The selectedNode ref doesn't seem necessary for multiple selections.
  // If you need to track the last selected node for some reason, you can keep this line.
  // Otherwise, it can be removed.
  selectedNode.value = newSelectedNodes.find(selectedNode => selectedNode.id === node.id) || null;
};

const nodeStatusDescription = computed(() => {
  const statusMap = {
    0: "waiting",
    1: "learning",
    2: "learning complete",
  };
  return selectedNode.value
    ? statusMap[selectedNode.value.status] || "Unknown status"
    : "";
});

const sortedSelectedNodes = computed(() => {
  if (!Array.isArray(props.modelValue)) {
    return []; // Return an empty array if props.modelValue is not an array
  }
  // Proceed with sorting if props.modelValue is an array
  return [...props.modelValue].sort((a, b) => a.name.localeCompare(b.name));
});
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
