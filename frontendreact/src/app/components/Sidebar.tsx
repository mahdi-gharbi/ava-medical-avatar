import { Link, useLocation } from 'react-router';
import {
  LayoutDashboard,
  GraduationCap,
  Briefcase,
  Sparkles,
  FileText,
  BarChart3,
  Database,
  BookOpen,
  FileSpreadsheet,
  Settings,
  Shield,
  Play,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  {
    name: 'AI Modes',
    items: [
      { name: 'Training & Simulation', href: '/training', icon: GraduationCap },
      { name: 'Start New Simulation', href: '/simulation-config', icon: Play },
      { name: 'Commercial Interaction', href: '/commercial', icon: Briefcase },
      { name: 'Marketing AI', href: '/marketing', icon: Sparkles },
      { name: 'Visit Intelligence', href: '/visit-intelligence', icon: FileText },
      { name: 'BO5 Reporting', href: '/bo5', icon: FileText },
    ],
  },
  {
    name: 'Analytics & Reports',
    items: [
      { name: 'Performance Analytics', href: '/analytics', icon: BarChart3 },
      { name: 'Reports', href: '/reports', icon: FileSpreadsheet },
    ],
  },
  {
    name: 'System',
    items: [
      { name: 'CRM Integration', href: '/crm', icon: Database },
      { name: 'Knowledge Base', href: '/knowledge-base', icon: BookOpen },
      { name: 'Settings', href: '/settings', icon: Settings },
      { name: 'Admin Panel', href: '/admin', icon: Shield },
    ],
  },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-white/80 backdrop-blur-xl border-r border-[#20AA99]/10 shadow-lg">
      <div className="h-full flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-[#20AA99]/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-lg">A</span>
            </div>
            <div>
              <h1 className="font-semibold text-[#2F748E]">AVA</h1>
              <p className="text-xs text-[#20AA99]">Medical Excellence</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-6 overflow-y-auto">
          {navigation.map((section, index) => (
            <div key={index}>
              {section.items ? (
                <div>
                  <p className="text-xs font-semibold text-[#2F748E]/60 mb-2 px-4">
                    {section.name}
                  </p>
                  <div className="space-y-1">
                    {section.items.map((item) => {
                      const isActive = location.pathname === item.href;
                      return (
                        <Link
                          key={item.name}
                          to={item.href}
                          className={`
                            flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200
                            ${
                              isActive
                                ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white shadow-lg shadow-[#20AA99]/30'
                                : 'text-[#2F748E]/70 hover:bg-[#F4FBFF] hover:text-[#20AA99]'
                            }
                          `}
                        >
                          <item.icon className="w-5 h-5" />
                          <span className="text-sm font-medium">{item.name}</span>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <Link
                  to={section.href}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200
                    ${
                      location.pathname === section.href
                        ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white shadow-lg shadow-[#20AA99]/30'
                        : 'text-[#2F748E]/70 hover:bg-[#F4FBFF] hover:text-[#20AA99]'
                    }
                  `}
                >
                  <section.icon className="w-5 h-5" />
                  <span className="text-sm font-medium">{section.name}</span>
                </Link>
              )}
            </div>
          ))}
        </nav>

        {/* Bottom section */}
        <div className="p-4 border-t border-[#20AA99]/10">
          <div className="p-4 rounded-lg bg-gradient-to-br from-[#20AA99]/10 to-[#8ABFA3]/10 border border-[#20AA99]/20">
            <p className="text-xs font-medium text-[#2F748E] mb-1">Need help?</p>
            <p className="text-xs text-[#20AA99]">Contact support</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
