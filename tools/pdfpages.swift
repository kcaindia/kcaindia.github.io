// Usage: swift tools/pdfpages.swift in.pdf outdir [widthPx]  -> prints page text, writes p1.png..pN.png
import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let out = a[2]
let target: CGFloat = a.count > 3 ? CGFloat(Double(a[3])!) : 1400
for i in 0..<doc.pageCount {
  let p = doc.page(at: i)!
  print("===== PAGE \(i+1) =====")
  print(p.string ?? "")
  let r = p.bounds(for: .mediaBox)
  let scale: CGFloat = target / r.width
  let img = p.thumbnail(of: NSSize(width: r.width*scale, height: r.height*scale), for: .mediaBox)
  if let t = img.tiffRepresentation, let b = NSBitmapImageRep(data: t), let png = b.representation(using: .png, properties: [:]) {
    try! png.write(to: URL(fileURLWithPath: "\(out)/p\(i+1).png"))
  }
}
