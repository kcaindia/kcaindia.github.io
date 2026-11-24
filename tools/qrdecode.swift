// Usage: swift tools/qrdecode.swift img1.png img2.png ...  -> prints the URL inside each QR code
import AppKit
import CoreImage
for p in CommandLine.arguments.dropFirst() {
  let ci = CIImage(contentsOf: URL(fileURLWithPath: p))!
  let det = CIDetector(ofType: CIDetectorTypeQRCode, context: nil, options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!
  print((p as NSString).lastPathComponent, det.features(in: ci).compactMap { ($0 as? CIQRCodeFeature)?.messageString })
}
