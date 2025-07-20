import streamlit as st
from graphviz import Digraph

# Generate DFS steps for visualization
def generate_steps(nums):
    steps = []
    counter = [0]

    def dfs(i, subset, parent_id):
        node_id = str(counter[0])
        counter[0] += 1
        label = f"{subset[:]}"
        steps.append(("node", node_id, label))  # Add node

        if parent_id is not None:
            steps.append(("edge", parent_id, node_id))  # Add edge

        if i == len(nums):
            return

        # Include nums[i]
        subset.append(nums[i])
        dfs(i + 1, subset, node_id)
        subset.pop()

        # Exclude nums[i]
        dfs(i + 1, subset, node_id)

    dfs(0, [], None)
    return steps

# Initialize Streamlit state
if "step" not in st.session_state:
    st.session_state.step = 0
if "steps" not in st.session_state:
    st.session_state.steps = []
if "nums" not in st.session_state:
    st.session_state.nums = []

st.set_page_config(page_title="Step-by-Step Subset Visualizer", layout="wide")
st.title("🪜 Step-by-Step Subset Visualizer (DFS)")

# User input
input_str = st.text_input("Enter numbers (comma-separated):", "1,2")

if st.button("Start Over"):
    try:
        nums = list(map(int, input_str.strip().split(",")))
        st.session_state.nums = nums
        st.session_state.steps = generate_steps(nums)
        st.session_state.step = 0
    except ValueError:
        st.error("Please enter valid integers.")

if st.session_state.steps:
    g = Digraph()
    added_nodes = set()

    # Render all steps up to current step
    for i in range(st.session_state.step + 1):
        action, *data = st.session_state.steps[i]
        if action == "node":
            node_id, label = data
            if node_id not in added_nodes:
                g.node(node_id, label)
                added_nodes.add(node_id)
        elif action == "edge":
            parent_id, child_id = data
            g.edge(parent_id, child_id)

    st.graphviz_chart(g)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Next Step"):
            if st.session_state.step < len(st.session_state.steps) - 1:
                st.session_state.step += 1
            else:
                st.warning("End of steps reached.")

    with col2:
        st.markdown(f"### Step {st.session_state.step + 1} of {len(st.session_state.steps)}")

