import QtQuick3D
import QtQuick3D.AssetUtils
import QtQuick3D.Helpers
import QtQuick3D.Particles3D
import QtQuick3D.Xr
import QtQuick 2.15

View3D {
    id: blochview
    anchors.fill: parent

    environment: SceneEnvironment {
        clearColor: "#112220"
    }

    property real yRotation: 0

    Node {
        id: scene
        eulerRotation.y: blochview.yRotation

        PerspectiveCamera {
            id: camera
            z: 300
        }

        DirectionalLight {
            z: 400
            brightness: 100
        }

        Model {
            source: "#Sphere"

            materials: DefaultMaterial {
                diffuseColor: "black"
                opacity: 0.2
            }
        }

        Model {

            source: "#Cylinder"

            scale: Qt.vector3d(0.15, 0.5, 0.15)

            position: Qt.vector3d(0, 1, 0)
            rotation: Qt.vector3d(1, 0, 1)

            materials: DefaultMaterial {
                diffuseColor: "black"
            }
        }

        Model {
            source: "#Cone"
            scale: Qt.vector3d(0.25, 0.15, 0.25)
            
        }
    }
}
