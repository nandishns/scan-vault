import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

interface SensitiveInfo {
  category: string;
  type: string;
  value: string;
}

interface SensitiveInfoSummaryProps {
  sensitiveInfo: SensitiveInfo[];
  onSave: () => void;
}

export function SensitiveInfoSummary({ sensitiveInfo, onSave }: SensitiveInfoSummaryProps) {
  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    onSave()
    setIsSaved(true)
  }

  const groupedInfo = sensitiveInfo.reduce((acc, info) => {
    if (!acc[info.category]) {
      acc[info.category] = [];
    }
    acc[info.category].push(info);
    return acc;
  }, {} as Record<string, SensitiveInfo[]>);

  return (
    <Card className="mt-4 max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Sensitive Information Summary</CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {Object.entries(groupedInfo).map(([category, items], index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger>{category}</AccordionTrigger>
              <AccordionContent>
                <ul className="list-disc pl-4">
                  {items.map((item, itemIndex) => (
                    <li key={itemIndex}>
                      <strong>{item.type}:</strong> {item.value}
                    </li>
                  ))}
                </ul>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
      <CardFooter>
        <Button onClick={handleSave} disabled={isSaved} className="w-full bg-blue-600 hover:bg-blue-700 text-white transition-colors">
          {isSaved ? 'Saved' : 'Save Summary'}
        </Button>
      </CardFooter>
    </Card>
  )
}

