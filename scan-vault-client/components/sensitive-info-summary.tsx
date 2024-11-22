import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

interface SensitiveInfoSummaryProps {
  results: {
    file_name: string;
    sensitive_fields: any[];
  };
}

export function SensitiveInfoSummary({ results }: SensitiveInfoSummaryProps) {
  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    setIsSaved(true)
  }

  // Transform the data for display
  const categories = {
    "Personally Identifiable Information": results.sensitive_fields.filter(field => field.category === "PII") || [],
    "Protected Health Information": results.sensitive_fields.filter(field => field.category === "PHI") || [],
    "Payment Card Information": results.sensitive_fields.filter(field => field.category === "PCI") || [],
  }

  return (
    <Card className="mt-4 max-w-2xl mx-auto">
      <CardHeader className="border-b">
        <CardTitle className="text-xl">Scan Results: {results.file_name}</CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <Accordion type="single" collapsible className="w-full">
          {Object.entries(categories).map(([category, items], index) => (
            items.length > 0 && (
              <AccordionItem key={index} value={`item-${index}`}>
                <AccordionTrigger className="text-lg font-medium">
                  {category} ({items.length})
                </AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-4">
                    {items.map((item, itemIndex) => (
                      <div key={itemIndex} className="p-4 bg-slate-50 rounded-lg border">
                        <div className="flex justify-between items-start mb-2">
                          <div className="flex-1">
                            <p className="font-medium capitalize text-base">
                              {item.type.replace(/_/g, ' ')}
                            </p>
                            <p className="text-lg font-semibold text-blue-600 mt-1">
                              {item.value}
                            </p>
                          </div>
                          <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                            item.confidence === 'high' ? 'bg-green-100 text-green-700' :
                            item.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {item.confidence.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">
                          <span className="font-medium">Context:</span> {item.context}
                        </p>
                      </div>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            )
          ))}
        </Accordion>
      </CardContent>
      <CardFooter className="border-t pt-6">
        <Button 
          onClick={handleSave} 
          disabled={isSaved} 
          className="w-full"
          variant={isSaved ? "outline" : "default"}
        >
          {isSaved ? '✓ Results Saved' : 'Save Results'}
        </Button>
      </CardFooter>
    </Card>
  )
}

