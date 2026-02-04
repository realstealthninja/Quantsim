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
              

              MouseArea {
                anchors.fill: parent
                // Check if the scroll event is for the MouseArea
                acceptedButtons: Qt.AllButtons

                // --- Key Logic: Handling the scroll event ---
                onWheel: (mouse) => {
                    // Check if scrollPixelDelta is available and non-zero
                    if (mouse.pixelDelta.x !== 0 || mouse.pixelDelta.y !== 0) {
                        // Use scrollPixelDelta.y for rotation around the Y-axis (vertical scroll)

                        // 1. Normalization: Multiply by a small factor (0.1) 
                        // to control sensitivity and make it feel right.
                        let delta = mouse.pixelDelta.y * 0.1

                        // 2. Apply the change to the rotation property
                        blochview.yRotation += delta

                        // Optional: Ensure rotatio n stays between 0 and 360 degrees
                        blochview.yRotation %= 360
                    }
                }
            }

            }

            Model {

              source: "#Cylinder"

              scale: Qt.vector3d(0.15, 0.5, 0.15)

              position: Qt.vector3d(0, 1, 0)

              materials: DefaultMaterial {
                diffuseColor: "black"
                
              }
            }


        }
    }
    
