import React, { useEffect, useMemo, useRef } from 'react';
import * as echarts from 'echarts';

import { GraphData, Message as MessageType } from '@/types';
import { lookupNodeColor, lookupNodeShape, selectGraphEmoji } from '@/utils';

type Props = {
  messages?: MessageType[];
};

const EChartsGraph: React.FC<Props> = ({ messages }) => {
  const chartRef = useRef<HTMLDivElement | null>(null);

  const graphData: GraphData | null = useMemo(() => {
    if (messages && messages.length) {
      const lastMessage = messages[messages.length - 1]; // Use the most recent message

      if (
        lastMessage?.graph &&
        lastMessage.graph.nodes?.length &&
        lastMessage.graph.edges?.length
      ) {
        // Get unique categories based on node type
        const uniqueTypes = Array.from(
          new Set(
            lastMessage.graph.nodes.map((node) => node?.type ?? 'Unknown')
          )
        );

        // Utility function to split by underscore and capitalize the first letter of each word
        const formatCategoryName = (type: string): string => {
          return type
            .split('_') // Split by underscore
            .map(
              (word) =>
                word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
            ) // Capitalize first letter
            .join(' '); // Join words back with a space
        };

        const categories = uniqueTypes.map((type) => ({
          name: formatCategoryName(type), // Format category name
          itemStyle: {
            color: lookupNodeColor(type), // Use the same color function for category
          },
        }));

        // Map nodes, assign a category based on the node type
        const nodes = lastMessage.graph.nodes.map((node) => {
          const metadata = JSON.parse(node?.metadata || '{}');

          const emoji = selectGraphEmoji(node?.type ?? 'Unknown');
          const { shape, icon } = lookupNodeShape(
            node?.type ?? 'Unknown',
            metadata?.type,
            metadata?.filetype
          );
          const color = lookupNodeColor(node?.type ?? 'Unknown');

          return {
            id: node?.id ?? 'unknown-id',
            name: `${node?.name ?? 'Unknown'}`,
            emoji,
            category: uniqueTypes.indexOf(node?.type ?? 'Unknown'),
            symbol: shape === 'image' && icon ? `image://${icon}` : shape,
            symbolSize: 20,
            itemStyle: {
              color,
            },
            metadata: metadata,
          };
        });

        // Map edges to links
        const links = lastMessage.graph.edges.map((edge) => ({
          source: edge?.from ?? 'unknown-source',
          target: edge?.to ?? 'unknown-target',
        }));

        return { nodes, links, categories };
      }
    }
    return null;
  }, [messages]);

  useEffect(() => {
    if (chartRef.current && graphData) {
      const chart = echarts.init(chartRef.current);

      const option = {
        tooltip: {
          formatter: function (params: any) {
            if (params.dataType === 'node') {
              // Access node metadata and format the tooltip
              const metadata = params.data.metadata || {};
              const type = metadata.type
                ? `<strong>Type:</strong> ${metadata.type}<br/>`
                : '';
              const fileType = metadata.filetype
                ? `<strong>File Type:</strong> ${metadata.filetype}<br/>`
                : '';
              const creationDate = metadata.creationDate
                ? `<strong>Created:</strong> ${metadata.creationDate}<br/>`
                : '';
              const description = metadata.description
                ? `<strong>Description:</strong> ${metadata.description}`
                : '';
              const uri = metadata.uri
                ? `<strong>URI:</strong> ${metadata.uri}`
                : '';

              return `
      <div style="width: 400px; word-wrap: break-word; overflow-wrap: break-word; white-space: normal;">
        <strong>${params.data.emoji} ${params.data.name}</strong><br/>
        <strong>ID:</strong> ${params.data.id}<br/>
        ${type}
        ${fileType}
        ${creationDate}
        ${description}
        ${uri}
      </div>
    `;
            }
            return '';
          },
        },
        legend: [
          {
            data: graphData.categories.map((c) => c.name),
            left: 'left',
          },
        ],
        series: [
          {
            type: 'graph',
            layout: 'force',
            data: graphData.nodes.map((node) => ({
              name: node.name,
              id: node.id,
              emoji: node.emoji,
              category: node.category,
              symbol: node.symbol,
              symbolSize: node.symbolSize,
              itemStyle: {
                color: node?.itemStyle?.color,
              },
              metadata: node.metadata,
            })),
            links: graphData.links,
            categories: graphData.categories, // Use categories with color
            roam: true,
            label: {
              show: true,
              position: 'right',
            },
            force: {
              repulsion: 200,
              edgeLength: [100, 200],
            },
            lineStyle: {
              opacity: 0.9,
              width: 1,
              curveness: 0.1,
            },
          },
        ],
      };

      chart.setOption(option);

      // Clean up the chart instance on component unmount
      return () => {
        chart.dispose();
      };
    }
  }, [graphData]);

  return <div ref={chartRef} style={{ width: '100%', height: '600px' }}></div>;
};

export default EChartsGraph;
