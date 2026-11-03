// Prints the face box (x,y,w,h in pixels, largest first) for each image given: swift faces.swift a.jpg b.jpg ...
import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print(path, "load-failed"); continue }
    let req = VNDetectFaceRectanglesRequest()
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([req])
    let W = CGFloat(cg.width), H = CGFloat(cg.height)
    var out: [String] = []
    for f in (req.results ?? []).sorted(by: { $0.boundingBox.width > $1.boundingBox.width }) {
        let b = f.boundingBox   // normalised, origin bottom-left
        let x = b.minX * W, y = (1 - b.maxY) * H, w = b.width * W, h = b.height * H
        out.append(String(format: "%.0f,%.0f,%.0f,%.0f", x, y, w, h))
    }
    print((path as NSString).lastPathComponent, Int(W), Int(H), out.joined(separator: " "))
}
