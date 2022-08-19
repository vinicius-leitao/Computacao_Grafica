from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math


class SphereApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Bola de futebol")
        self.size(800, 800)

        # OpenGL Initialization
        GL.glClearColor(0.1, 0.5, 0.1, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(self.pipeline)

        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/bola.jpg")
        GL.glUniform1i(GL.glGetUniformLocation(
            self.pipeline, "textureSlot"), 0)

        self.a = 0
        self.r = 1
        self.sphereArrayBufferId = None

    def coordenadaEsferica(self, i, j, n):
        theta = i*2*math.pi/n
        phi = j*math.pi/n-math.pi/2
        return (phi, theta)

    def drawSphere(self):
        n = 50
        if self.sphereArrayBufferId == None:
            position = array('f')
            uvs = array('f')
            for i in range(0, n):
                for j in range(0, n):
                    uvs.append(j/(n-1))
                    uvs.append(i/(n-1))
                    phi, theta = self.coordenadaEsferica(i, j, n)
                    position.append(math.cos(theta)*math.cos(phi))
                    position.append(math.sin(phi))
                    position.append(math.sin(theta)*math.cos(phi))
                    uvs.append(j/(n-1))
                    uvs.append((i-1)/(n-1))
                    phi2, theta2 = self.coordenadaEsferica(i-1, j, n)
                    position.append(math.cos(theta2)*math.cos(phi2))
                    position.append(math.sin(phi2))
                    position.append(math.sin(theta2)*math.cos(phi2))

            self.sphereArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.sphereArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)

            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize,
                            ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(
                0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))

            idUvBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idUvBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(
                uvs)*uvs.itemsize, ctypes.c_void_p(uvs.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(
                1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))

        GL.glBindVertexArray(self.sphereArrayBufferId)
        projection = glm.perspective(
            math.pi/4, self.width/self.height, 0.1, 100)
        camera = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0), glm.vec3(0, 1, 0))
        model = glm.rotate(self.a, glm.vec3(0, 0, 1)) * glm.rotate(self.a,
                                                                   glm.vec3(0, 1, 0)) * glm.rotate(self.a, glm.vec3(1, 0, 0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(
            self.pipeline, "MVP"), 1, GL.GL_FALSE, glm.value_ptr(mvp))
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 2*n*n)
        self.a += 0.01

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        # Draw a Dotted Sphere
        self.drawSphere()


SphereApp()
