// Face box + landmarks (pixels, origin top-left) as JSON lines.
import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil), let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("{\"file\":\"\(path)\",\"err\":1}"); continue }
    let req = VNDetectFaceLandmarksRequest()
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([req])
    let W = CGFloat(cg.width), H = CGFloat(cg.height)
    guard let f = (req.results ?? []).sorted(by: { $0.boundingBox.width > $1.boundingBox.width }).first else { print("{\"file\":\"\(path)\",\"err\":2}"); continue }
    let b = f.boundingBox
    func pts(_ r: VNFaceLandmarkRegion2D?) -> [[Double]] {
        guard let r = r else { return [] }
        return r.pointsInImage(imageSize: CGSize(width: W, height: H)).map { [Double($0.x), Double(H - $0.y)] }
    }
    let l = f.landmarks
    let d: [String: Any] = ["file": (path as NSString).lastPathComponent, "W": Int(W), "H": Int(H),
        "box": [Double(b.minX * W), Double((1 - b.maxY) * H), Double(b.width * W), Double(b.height * H)],
        "roll": f.roll?.doubleValue ?? 0, "yaw": f.yaw?.doubleValue ?? 0,
        "leftPupil": pts(l?.leftPupil), "rightPupil": pts(l?.rightPupil), "contour": pts(l?.faceContour), "nose": pts(l?.noseCrest), "leftEye": pts(l?.leftEye), "rightEye": pts(l?.rightEye), "outerLips": pts(l?.outerLips), "leftBrow": pts(l?.leftEyebrow), "rightBrow": pts(l?.rightEyebrow)]
    let j = try! JSONSerialization.data(withJSONObject: d)
    print(String(data: j, encoding: .utf8)!)
}
