# Vue.js Interview Ready Guide

## 1. Vue Setup: CLI vs CDN

### What's the Difference?

**CDN (Content Delivery Network)**: Quick setup, include Vue via `<script>` tag  
**CLI (Command Line Interface)**: Full development environment with build tools

### Comparison Table

|Feature|CDN|CLI|
|---|---|---|
|**Setup Time**|⚡ Instant|⏱️ 2-3 minutes|
|**Use Case**|Small projects, prototypes|Production apps|
|**Build Tools**|❌ None|✅ Vite/Webpack|
|**Single File Components**|❌ No|✅ Yes (.vue files)|
|**Hot Reload**|❌ No|✅ Yes|
|**npm Packages**|❌ Limited|✅ Full access|
|**File Size**|⚠️ Larger|✅ Optimized|
|**TypeScript**|❌ No|✅ Yes|
|**Best For**|Learning, demos|Real applications|

---

### CDN Setup (Quick Start)

**Use when:** Learning Vue, small projects, quick prototypes

**Setup:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Vue CDN Example</title>
  <!-- Include Vue from CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="count++">Count: {{ count }}</button>
    <input v-model="name" placeholder="Enter name">
    <p>Hello, {{ name }}!</p>
  </div>

  <script>
    const { createApp } = Vue

    createApp({
      data() {
        return {
          message: 'Hello Vue!',
          count: 0,
          name: ''
        }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

**Pros:**

- ✅ No installation needed
- ✅ Works immediately in browser
- ✅ Great for learning
- ✅ One HTML file

**Cons:**

- ❌ No component files (.vue)
- ❌ No build optimization
- ❌ Limited to browser features
- ❌ Harder to organize large apps

**When to Use:**

- Quick experiments
- Learning Vue basics
- Simple landing pages
- Code demos/tutorials

---

### CLI Setup (Production Ready)

**Use when:** Building real applications, team projects, production deployment

**Setup:**

**Step 1: Install Node.js** (Download from nodejs.org)

**Step 2: Create Vue Project**

```bash
# Create project
npm create vue@latest

# Follow prompts:
✔ Project name: my-app
✔ Add TypeScript? No
✔ Add Vue Router? Yes
✔ Add Pinia? Yes
✔ Add ESLint? Yes

# Navigate and install
cd my-app
npm install

# Run development server
npm run dev
```

**Step 3: Project Structure**

```
my-app/
├── src/
│   ├── components/      # Reusable components
│   │   └── HelloWorld.vue
│   ├── views/          # Page components
│   │   └── HomeView.vue
│   ├── router/         # Route configuration
│   │   └── index.js
│   ├── stores/         # Pinia stores
│   │   └── counter.js
│   ├── App.vue         # Root component
│   └── main.js         # Entry point
├── public/             # Static assets
├── index.html
├── package.json        # Dependencies
└── vite.config.js      # Build config
```

**Step 4: Component Example**

```vue
<!-- src/components/Counter.vue -->
<template>
  <div class="counter">
    <h2>{{ title }}</h2>
    <button @click="increment">Count: {{ count }}</button>
  </div>
</template>

<script>
export default {
  props: {
    title: String
  },
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>

<style scoped>
.counter {
  padding: 20px;
  border: 2px solid #42b883;
}
</style>
```

**Step 5: Use Component**

```vue
<!-- src/App.vue -->
<template>
  <div>
    <Counter title="My Counter" />
  </div>
</template>

<script>
import Counter from './components/Counter.vue'

export default {
  components: { Counter }
}
</script>
```

**Pros:**

- ✅ Single File Components (.vue)
- ✅ Hot Module Replacement (instant updates)
- ✅ npm packages (Vue Router, Pinia, Axios, etc.)
- ✅ Build optimization (code splitting, minification)
- ✅ TypeScript support
- ✅ ESLint for code quality
- ✅ Better project organization

**Cons:**

- ❌ Requires Node.js installation
- ❌ Build step needed
- ❌ Steeper learning curve
- ❌ More complex setup

**When to Use:**

- Production applications
- Large projects
- Team collaboration
- When you need routing, state management
- Projects requiring npm packages

---

### Side-by-Side Example

**Same Counter App:**

**CDN Version (One File):**

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/vue@3"></script>
  <style>
    .counter { padding: 20px; border: 2px solid #42b883; }
  </style>
</head>
<body>
  <div id="app">
    <div class="counter">
      <h2>My Counter</h2>
      <button @click="count++">Count: {{ count }}</button>
    </div>
  </div>

  <script>
    Vue.createApp({
      data() {
        return { count: 0 }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

**CLI Version (Organized Files):**

```vue
<!-- Counter.vue -->
<template>
  <div class="counter">
    <h2>My Counter</h2>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return { count: 0 }
  }
}
</script>

<style scoped>
.counter { padding: 20px; border: 2px solid #42b883; }
</style>
```

---

### Build Commands (CLI)

```bash
# Development (with hot reload)
npm run dev

# Production build (optimized)
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Lint code
npm run lint
```

---

### Interview Question: CLI vs CDN?

**Q: When would you use CDN vs CLI?**

**Answer:**

- **CDN**: Quick demos, learning, simple pages with no build requirements
- **CLI**: Production apps needing components, routing, state management, and npm packages. CLI provides better development experience, code organization, and optimized builds.

**Q: Can you mix both?**

**Answer:** Yes, but not recommended. You can use Vue Router via CDN, but lose benefits like code splitting. For production, always use CLI.

---

## 2. Core Concepts

### What is Vue.js?

**Vue.js** is a progressive JavaScript framework for building user interfaces and single-page applications.

**Key Features:**

- ✅ Reactive data binding
- ✅ Component-based architecture
- ✅ Virtual DOM for performance
- ✅ Easy learning curve

### Reactivity Flow

```
User Action → Data Changes → Virtual DOM Update → Real DOM Patch
```

### Template Syntax (Must Know)

```html
<!-- 1. Text Interpolation -->
<p>{{ message }}</p>

<!-- 2. Attribute Binding (v-bind or :) -->
<img :src="imageUrl" :alt="description">

<!-- 3. Event Handling (v-on or @) -->
<button @click="increment">Click</button>

<!-- 4. Two-Way Binding (v-model) -->
<input v-model="username">

<!-- 5. Conditional Rendering -->
<p v-if="isLoggedIn">Welcome!</p>
<p v-else>Please login</p>

<!-- 6. List Rendering -->
<li v-for="user in users" :key="user.id">{{ user.name }}</li>

<!-- 7. Class Binding -->
<div :class="{ active: isActive, 'text-danger': hasError }"></div>

<!-- 8. Style Binding -->
<div :style="{ color: textColor, fontSize: size + 'px' }"></div>
```

### Basic Component Structure

```vue
<template>
  <div>
    <h1>{{ title }}</h1>
    <button @click="increment">Count: {{ count }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: 'My App',
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  },
  computed: {
    doubleCount() {
      return this.count * 2
    }
  }
}
</script>

<style scoped>
h1 { color: #42b883; }
</style>
```

**Interview Tip:** Explain that `scoped` keeps styles isolated to this component only.

---

## 2. Components & Communication

### Props (Parent → Child)

```vue
<!-- Parent.vue -->
<template>
  <UserCard 
    name="Alice" 
    :age="25" 
    :is-admin="true" 
  />
</template>

<!-- UserCard.vue -->
<script>
export default {
  props: {
    name: { type: String, required: true },
    age: { type: Number, default: 0 },
    isAdmin: Boolean
  }
}
</script>
```

**Key Points:**

- Props flow **downward** (one-way binding)
- Never mutate props in child
- Use `:` for dynamic values

### Emits (Child → Parent)

```vue
<!-- Child.vue -->
<template>
  <button @click="sendMessage">Send</button>
</template>

<script>
export default {
  emits: ['message-sent'],
  methods: {
    sendMessage() {
      this.$emit('message-sent', { text: 'Hello', id: 1 })
    }
  }
}
</script>

<!-- Parent.vue -->
<template>
  <Child @message-sent="handleMessage" />
</template>

<script>
export default {
  methods: {
    handleMessage(data) {
      console.log('Received:', data)
    }
  }
}
</script>
```

**Flow Diagram:**

```
Parent Component (data)
    ↓ props
Child Component
    ↓ $emit
Parent Component (event handler)
```

---

## 3. Vue Router

### Basic Setup

**Install:**

```bash
npm install vue-router@4
```

**Configure Routes:**

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/user/:id', component: User }  // Dynamic route
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

**Use in App:**

```vue
<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
  </nav>
  <router-view></router-view>
</template>
```

### Navigation Methods

```javascript
// In component methods
this.$router.push('/about')
this.$router.push({ path: '/user/123' })
this.$router.push({ name: 'User', params: { id: 123 }})
this.$router.go(-1)  // Go back
```

### Access Route Params

```vue
<template>
  <div>User ID: {{ $route.params.id }}</div>
</template>

<script>
export default {
  mounted() {
    console.log(this.$route.params.id)
    console.log(this.$route.query.page)  // Query params
  }
}
</script>
```

### Route Guards (Authentication)

```javascript
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isLoggedIn()) {
    next('/login')
  } else {
    next()
  }
})
```

**Interview Question:** How do you protect routes? Use navigation guards!

---

## 4. State Management

### Pinia (Modern, Recommended)

**Install:**

```bash
npm install pinia
```

**Create Store:**

```javascript
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    users: []
  }),
  
  getters: {
    doubleCount: (state) => state.count * 2
  },
  
  actions: {
    increment() {
      this.count++
    },
    async fetchUsers() {
      this.users = await fetch('/api/users').then(r => r.json())
    }
  }
})
```

**Use in Component:**

```vue
<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<template>
  <div>
    Count: {{ counter.count }}
    <button @click="counter.increment">+</button>
  </div>
</template>
```

### Vuex (Classic)

```javascript
import { createStore } from 'vuex'

export default createStore({
  state: { count: 0 },
  mutations: {
    INCREMENT(state) { state.count++ }
  },
  actions: {
    incrementAsync({ commit }) {
      setTimeout(() => commit('INCREMENT'), 1000)
    }
  },
  getters: {
    doubleCount: state => state.count * 2
  }
})
```

**Comparison:**

|Feature|Pinia|Vuex|
|---|---|---|
|Mutations|❌ Not needed|✅ Required|
|TypeScript|✅ Better|⚠️ OK|
|Syntax|✅ Simpler|⚠️ Verbose|
|Recommendation|✅ New projects|⚠️ Legacy|

---

## 5. HTTP Requests

### Axios Setup

**Install:**

```bash
npm install axios
```

**Create API Service:**

```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
})

// Add auth token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default {
  getUsers: () => api.get('/users'),
  createUser: (data) => api.post('/users', data),
  updateUser: (id, data) => api.put(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`)
}
```

### Use in Component

```vue
<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <ul v-else>
      <li v-for="user in users" :key="user.id">{{ user.name }}</li>
    </ul>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  data() {
    return {
      users: [],
      loading: false,
      error: null
    }
  },
  
  async mounted() {
    this.loading = true
    try {
      const { data } = await api.getUsers()
      this.users = data
    } catch (err) {
      this.error = err.message
    } finally {
      this.loading = false
    }
  }
}
</script>
```

---

## 6. Lifecycle Hooks

### Hook Flow

```
beforeCreate → created → beforeMount → mounted
                                          ↓
                                       (updates)
                                          ↓
                              beforeUpdate → updated
                                          ↓
                              beforeUnmount → unmounted
```

### Common Uses

```vue
<script>
export default {
  created() {
    // Component initialized, data available
    // Good for: Setting up data, no DOM access
    console.log('Created')
  },
  
  mounted() {
    // Component in DOM
    // Good for: API calls, DOM manipulation, timers
    this.fetchData()
    this.timer = setInterval(() => {}, 1000)
  },
  
  updated() {
    // After data changes and re-render
    // Good for: Responding to DOM updates
  },
  
  unmounted() {
    // Component removed from DOM
    // Good for: Cleanup (clear timers, remove listeners)
    clearInterval(this.timer)
  }
}
</script>
```

**Interview Question:** When to fetch data? **Answer:** In `mounted()` hook when you need DOM access, or `created()` for simple data setup.

---

## 7. Composition API vs Options API

### Options API (Traditional)

```vue
<script>
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() { this.count++ }
  },
  computed: {
    double() { return this.count * 2 }
  },
  mounted() {
    console.log('Mounted')
  }
}
</script>
```

### Composition API (Modern)

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const double = computed(() => count.value * 2)

function increment() {
  count.value++
}

onMounted(() => {
  console.log('Mounted')
})
</script>
```

### Key Differences

|Feature|Options API|Composition API|
|---|---|---|
|Syntax|Separate sections|Grouped by logic|
|Code Reuse|Mixins|Composables|
|TypeScript|⚠️ OK|✅ Better|
|Learning|✅ Easier|⚠️ Steeper|

### Composable (Reusable Logic)

```javascript
// composables/useFetch.js
import { ref } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const loading = ref(false)
  
  async function fetchData() {
    loading.value = true
    data.value = await fetch(url).then(r => r.json())
    loading.value = false
  }
  
  return { data, loading, fetchData }
}
```

```vue
<script setup>
import { useFetch } from '@/composables/useFetch'

const { data, loading, fetchData } = useFetch('/api/users')
onMounted(fetchData)
</script>
```

---

## 9. Common Interview Questions

### Q1: CDN vs CLI - When to use each?

**Answer:**

- **CDN**: For learning, quick prototypes, simple pages. Include Vue via `<script>` tag - no build tools needed.
- **CLI**: For production apps. Provides Single File Components, hot reload, npm packages, optimized builds, and better project organization.

### Q2: What is Vue.js?

**Answer:** Progressive JavaScript framework for building UIs using component-based architecture, reactive data binding, and virtual DOM.

### Q3: v-if vs v-show?

**Answer:**

- `v-if`: Removes element from DOM (conditional rendering)
- `v-show`: Hides with CSS `display: none`
- Use `v-show` for frequent toggling (better performance)

### Q4: What is Virtual DOM?

**Answer:** Lightweight copy of real DOM. Vue updates Virtual DOM first, compares with real DOM, then applies only necessary changes (efficient).

### Q5: Computed vs Methods?

**Answer:**

- **Computed**: Cached, only recalculates when dependencies change
- **Methods**: Executes every time called
- Use computed for derived data

### Q6: How do components communicate?

**Answer:**

- Parent → Child: **Props**
- Child → Parent: **$emit** events
- Siblings/Global: **Pinia/Vuex**

### Q7: What is :key in v-for?

**Answer:** Unique identifier for Vue to track elements efficiently. Required for proper list updates and performance.

### Q8: What is v-model?

**Answer:** Two-way data binding shorthand for `:value` + `@input`. Syncs input with data automatically.

### Q9: Options API vs Composition API?

**Answer:**

- **Options API**: Traditional, easier for beginners
- **Composition API**: Better code organization, reusability, TypeScript support

### Q10: What are lifecycle hooks?

**Answer:** Special methods called at component stages: `created`, `mounted`, `updated`, `unmounted`. Used for setup, API calls, cleanup.

### Q11: How to optimize Vue app?

**Answer:**

- Use `v-show` for frequent toggles
- Use `:key` in `v-for`
- Lazy load components
- Use computed properties
- Implement virtual scrolling for long lists

---

## 10. Complete Project Example

### Project: Task Manager (Vue + Flask)

This example demonstrates all key concepts in a working application.

### Project Structure

```
task-manager/
├── backend/              # Flask API
│   ├── app.py
│   └── requirements.txt
├── frontend/             # Vue App
│   ├── src/
│   │   ├── components/
│   │   │   └── TaskItem.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   └── About.vue
│   │   ├── stores/
│   │   │   └── tasks.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
```

### Backend (Flask)

**app.py**

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {'id': 1, 'title': 'Learn Vue', 'completed': False},
    {'id': 2, 'title': 'Build Project', 'completed': False}
]

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    task = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        'completed': False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if task:
        task['completed'] = request.json['completed']
        return jsonify(task)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
```

**requirements.txt**

```
Flask==3.0.0
Flask-CORS==4.0.0
```

### Frontend (Vue)

**main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

**router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

**services/api.js**

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api'
})

export default {
  getTasks: () => api.get('/tasks'),
  createTask: (task) => api.post('/tasks', task),
  updateTask: (id, task) => api.put(`/tasks/${id}`, task),
  deleteTask: (id) => api.delete(`/tasks/${id}`)
}
```

**stores/tasks.js**

```javascript
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    loading: false
  }),
  
  getters: {
    completedTasks: (state) => state.tasks.filter(t => t.completed),
    activeTasks: (state) => state.tasks.filter(t => !t.completed)
  },
  
  actions: {
    async fetchTasks() {
      this.loading = true
      const { data } = await api.getTasks()
      this.tasks = data
      this.loading = false
    },
    
    async addTask(title) {
      const { data } = await api.createTask({ title })
      this.tasks.push(data)
    },
    
    async toggleTask(task) {
      const { data } = await api.updateTask(task.id, {
        completed: !task.completed
      })
      const index = this.tasks.findIndex(t => t.id === task.id)
      this.tasks[index] = data
    },
    
    async removeTask(id) {
      await api.deleteTask(id)
      this.tasks = this.tasks.filter(t => t.id !== id)
    }
  }
})
```

**components/TaskItem.vue**

```vue
<template>
  <div class="task-item" :class="{ completed: task.completed }">
    <input 
      type="checkbox" 
      :checked="task.completed"
      @change="$emit('toggle', task)"
    >
    <span>{{ task.title }}</span>
    <button @click="$emit('delete', task.id)">Delete</button>
  </div>
</template>

<script>
export default {
  props: {
    task: { type: Object, required: true }
  },
  emits: ['toggle', 'delete']
}
</script>

<style scoped>
.task-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  margin: 5px 0;
}

.completed span {
  text-decoration: line-through;
  color: #999;
}
</style>
```

**views/Home.vue**

```vue
<template>
  <div class="home">
    <h1>Task Manager</h1>
    
    <form @submit.prevent="addTask">
      <input v-model="newTask" placeholder="Add new task">
      <button type="submit">Add</button>
    </form>
    
    <div v-if="store.loading">Loading...</div>
    
    <div v-else>
      <h2>Active Tasks ({{ store.activeTasks.length }})</h2>
      <TaskItem
        v-for="task in store.activeTasks"
        :key="task.id"
        :task="task"
        @toggle="store.toggleTask"
        @delete="store.removeTask"
      />
      
      <h2>Completed Tasks ({{ store.completedTasks.length }})</h2>
      <TaskItem
        v-for="task in store.completedTasks"
        :key="task.id"
        :task="task"
        @toggle="store.toggleTask"
        @delete="store.removeTask"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import TaskItem from '@/components/TaskItem.vue'

const store = useTaskStore()
const newTask = ref('')

onMounted(() => {
  store.fetchTasks()
})

function addTask() {
  if (newTask.value.trim()) {
    store.addTask(newTask.value)
    newTask.value = ''
  }
}
</script>

<style scoped>
.home { max-width: 600px; margin: 0 auto; padding: 20px; }
form { display: flex; gap: 10px; margin: 20px 0; }
input { flex: 1; padding: 10px; }
</style>
```

**views/About.vue**

```vue
<template>
  <div class="about">
    <h1>About Task Manager</h1>
    <p>Built with Vue 3 and Flask</p>
    <router-link to="/">Back to Tasks</router-link>
  </div>
</template>
```

**App.vue**

```vue
<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; }
nav {
  background: #42b883;
  padding: 20px;
  display: flex;
  gap: 20px;
}
nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
nav a.router-link-active {
  text-decoration: underline;
}
</style>
```

### Setup and Run Instructions

**1. Backend Setup:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Server runs on http://localhost:5000
```

**2. Frontend Setup:**

```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

**3. Test the Application:**

- Open browser to `http://localhost:5173`
- Add tasks
- Toggle completion
- Delete tasks
- Navigate between Home and About

### Key Concepts Demonstrated

✅ **Components**: TaskItem component with props and emits  
✅ **State Management**: Pinia store for global state  
✅ **API Calls**: Axios service for HTTP requests  
✅ **Routing**: Vue Router with navigation  
✅ **Lifecycle**: onMounted hook for data fetching  
✅ **Composition API**: Script setup with ref, computed  
✅ **Directives**: v-for, v-if, v-model, @click  
✅ **Forms**: Form handling and validation  
✅ **Styling**: Scoped styles and dynamic classes

---

## 📚 Additional Resources

- **Official Docs**: https://vuejs.org
- **Vue Router**: https://router.vuejs.org
- **Pinia**: https://pinia.vuejs.org
- **Vue Mastery**: https://www.vuemastery.com

## ✅ Interview Checklist

Before your interview, make sure you can:

- [ ] Explain CLI vs CDN setup
- [ ] Explain Vue's reactivity system
- [ ] Create components with props and emits
- [ ] Set up Vue Router with navigation
- [ ] Use Pinia/Vuex for state management
- [ ] Make API calls with Axios
- [ ] Understand lifecycle hooks
- [ ] Explain v-if vs v-show
- [ ] Use v-for with :key
- [ ] Difference between Options and Composition API
- [ ] Build a simple CRUD app

**Good luck with your interview! 🚀**