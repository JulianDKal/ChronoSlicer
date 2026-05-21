<template>
  <div ref="container" class="three-container"></div>
</template>

<style scoped>
.three-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
}
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import * as THREE from 'three'
import eventBus from '../eventBus'

const container = ref(null)
let scene, camera, renderer
let rectangleFrame
let controls
let lineObject //THREE.LineSegments

const initThree = () => {
  // Setup scene with WHITE background
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xffffff) // White background
  
  // Setup orthographic camera for 2D view
  const aspect = window.innerWidth / window.innerHeight
  const viewSize = 10 // Show from -10 to 10 in world coordinates
  
  camera = new THREE.OrthographicCamera(
    -viewSize * aspect, // left
    viewSize * aspect,  // right
    viewSize,           // top
    -viewSize,          // bottom
    0.1,                // near
    1000                // far
  )
  camera.position.z = 5
  camera.lookAt(0, 0, 0)
  
  // Setup renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setClearColor(0xffffff) // White clear color
  container.value.appendChild(renderer.domElement)

  controls = new OrbitControls(camera, renderer.domElement)
  
  controls.enableZoom = true
  controls.zoomSpeed = 1.0
  controls.enablePan = true
  controls.panSpeed = 1.0
  controls.enableRotate = false  // Disable rotation for 2D
  
  // Pan limits (optional)
  controls.maxZoom = 5
  controls.minZoom = 0.2
  
  // For orthographic camera
  controls.screenSpacePanning = true 
  
  drawRectangleFrame()
  animate();
  
}

async function handleDownloadRequest() {
  console.log('Download request received in ThreeViewer') 
  try {
    const response = await fetch('/api/save_pdf')
    if (!response.ok) {
      throw new Error('Failed to save PDF')
    }
    else {
      console.log('PDF save request successful')
    }
  } catch (error) {
    console.error('Error saving PDF:', error)
  }
}

const handleLinesUpdate = (lines) => {
  console.log('Received via event bus:', lines)
  drawObjects(lines)
}

const drawObjects = (data) => {
  if (!data || data.length === 0) {
    console.warn('No lines to draw')
    return
  }

  // Clear existing lines if any
  if (lineObject) {
    scene.remove(lineObject)
  }

  // Build vertices array
  const vertices = []
  const curves = [] //THREE.Line[]
  const colors = []
  
  data.forEach(object => {
    if(object.type === 'l') {
      vertices.push(object.x1, object.y1, 0)
      vertices.push(object.x2, object.y2, 0)
      // Parse color (convert hex to RGB 0-1 range)
      const colorHex = object.color || '#000000'
      const r = parseInt(colorHex.slice(1, 3), 16) / 255
      const g = parseInt(colorHex.slice(3, 5), 16) / 255
      const b = parseInt(colorHex.slice(5, 7), 16) / 255
      
      // Each vertex needs its own color (same for both ends of the line)
      colors.push(r, g, b)  // First vertex
      colors.push(r, g, b)  // Second vertex
    }
    else if(object.type === 'c') {
        const curve = new THREE.CubicBezierCurve(
          new THREE.Vector3(object.x1, object.y1, 0),
          new THREE.Vector3(object.x2, object.y2, 0),
          new THREE.Vector3(object.x3, object.y3, 0),
          new THREE.Vector3(object.x4, object.y4, 0)
        )
        
        const points = curve.getPoints(20) // Get 20 points along the curve
        const geometry = new THREE.BufferGeometry().setFromPoints(points)
        //TODO: Make it so we don't create a new material for each curve
        // console.log(`Curve color: ${object.color}`)
        const material = new THREE.LineBasicMaterial({ color: object.color, linewidth: 2 })
        const curveObject = new THREE.Line(geometry, material)
        curves.push(curveObject)
    }
    else if(object.type === 'mbox') {
      console.log('MediaBox data received:', object.w, " ", object.h)
      // Optionally, we could use this to adjust the camera view or scaling
    }
    
  })

  if (vertices.length === 0) {
    console.warn('No valid vertices found')
    return
  }

  // Create geometry and material
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices), 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(colors), 3))
  
  const material = new THREE.LineBasicMaterial({ color: 0xffffff, vertexColors: true, linewidth: 2 })
  
  // Create and add line segments
  lineObject = new THREE.Group()

  const lineSegments = new THREE.LineSegments(geometry, material)
  lineObject.add(lineSegments)
  curves.forEach(curve => lineObject.add(curve))

  scene.add(lineObject)
  
  console.log(`Drew ${data.length} line segments and ${curves.length} curves`)
}

const drawRectangleFrame = () => {
  // Define rectangle boundaries (from -11 to 5 in X, -4 to 8 in Y)


  const left = -11
  const right = 5
  const top = 8
  const bottom = -4
  
  // Create vertices for the rectangle (4 lines: top, right, bottom, left)
  const vertices = new Float32Array([
    // Top edge (left to right)
    left, top, 0,
    right, top, 0,
    // Right edge (top to bottom)
    right, top, 0,
    right, bottom, 0,
    // Bottom edge (right to left)
    right, bottom, 0,
    left, bottom, 0,
    // Left edge (bottom to top)
    left, bottom, 0,
    left, top, 0
  ])
  
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
  
  const material = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 })
  rectangleFrame = new THREE.LineSegments(geometry, material)
  scene.add(rectangleFrame)
  
  console.log('Rectangle frame drawn:', { left, right, top, bottom })
}

const animate = () => {
  requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
}

const handleResize = () => {
  const aspect = window.innerWidth / window.innerHeight
  const viewSize = 10
  
  camera.left = -viewSize * aspect
  camera.right = viewSize * aspect
  camera.top = viewSize
  camera.bottom = -viewSize
  camera.updateProjectionMatrix()
  
  renderer.setSize(window.innerWidth, window.innerHeight)
}

onMounted(() => {
  initThree()
  // loadAndDrawLines()
  window.addEventListener('resize', handleResize)
  eventBus.on('lines-updated', handleLinesUpdate)
  eventBus.on('save_pdf_request', () => {
    handleDownloadRequest()
  })  
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (renderer) renderer.dispose()
})
  eventBus.off('lines-updated', handleLinesUpdate)
</script>

<style scoped>
.three-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>